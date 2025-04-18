from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Disease
from django.db.models import Q

# Create your views here.
class DialogflowWebhook(APIView):
    def post(self, request):
        # Lấy dữ liệu từ yêu cầu Dialogflow
        data = request.data
        print(data)
        action = data.get('queryResult', {}).get('action', '')
        parameters = data.get('queryResult', {}).get('parameters', {})
        contexts = data.get('queryResult', {}).get('outputContexts', [])

        # Lấy DiseaseName từ parameters hoặc context
        disease_name = parameters.get('DiseaseName', '').lower()
        if not disease_name:
            # Kiểm tra context disease_context
            for context in contexts:
                if 'disease_context' in context.get('name', ''):
                    disease_name = context.get('parameters', {}).get('DiseaseName', '').lower()
                    break

        # Xử lý các action
        fulfillment_text = "Xin lỗi, tôi không hiểu yêu cầu của bạn. Hãy thử lại."

        if action == 'get_disease_definitions':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"**Định nghĩa của {disease.name}**: {disease.definition}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_disease_symptoms':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"**Triệu chứng của {disease.name}**: {disease.symptoms}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_disease_treatments':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"**Phương pháp điều trị {disease.name}**: {disease.treatments}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_disease_causes':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"**Nguyên nhân của {disease.name}**: {disease.cause}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_disease_by_symptoms':
            symptoms = parameters.get('Symptoms', '').lower()
            if symptoms:
                diseases = Disease.objects.filter(symptoms__icontains=symptoms)
                if diseases:
                    disease_names = [d.name for d in diseases]
                    fulfillment_text = f"Các bệnh có thể liên quan đến triệu chứng '{symptoms}': {', '.join(disease_names)}."
                else:
                    fulfillment_text = f"Không tìm thấy bệnh nào khớp với triệu chứng '{symptoms}'."
            else:
                fulfillment_text = "Vui lòng mô tả triệu chứng cụ thể hơn."

        elif action == 'get_general_disease_info':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = (
                    f"**Thông tin về {disease.name}**\n"
                    f"Định nghĩa: {disease.definition}\n"
                    f"Triệu chứng: {disease.symptoms}\n"
                    f"Phương pháp điều trị: {disease.treatments}\n"
                    f"Nguyên nhân: {disease.cause}"
                )
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_follow_up_info':
            # Xử lý câu hỏi tiếp nối dựa trên câu hỏi trước
            query_text = data.get('queryResult', {}).get('queryText', '').lower()
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                if 'triệu chứng' in query_text:
                    fulfillment_text = f"**Triệu chứng của {disease.name}**: {disease.symptoms}"
                elif 'điều trị' in query_text or 'chữa' in query_text:
                    fulfillment_text = f"**Phương pháp điều trị {disease.name}**: {disease.treatments}"
                elif 'nguyên nhân' in query_text or 'tại sao' in query_text:
                    fulfillment_text = f"**Nguyên nhân của {disease.name}**: {disease.cause}"
                else:
                    fulfillment_text = f"**Thông tin về {disease.name}**: {disease.definition}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        # Định dạng phản hồi cho Dialogflow
        response = {
            "fulfillmentText": fulfillment_text,
            "source": "webhook"
        }
        return Response(response, status=status.HTTP_200_OK)