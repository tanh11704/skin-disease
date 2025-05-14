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
        print(f"data: {data}")
        action = data.get('queryResult', {}).get('action', '')
        parameters = data.get('queryResult', {}).get('parameters', {})
        contexts = data.get('queryResult', {}).get('outputContexts', [])

        # Lấy DiseaseName từ parameters hoặc context
        disease_name = parameters.get('skin', '').lower()
        if not disease_name:
            # Kiểm tra context disease_context
            for context in contexts:
                if 'tuvanbenh-khoidong-followup' in context.get('name', ''):
                    disease_name = context.get('parameters', {}).get('skin', '').lower()
                    break

        # Xử lý các action
        fulfillment_text = "Xin lỗi, tôi không hiểu yêu cầu của bạn. Hãy thử lại."
        print(f"disease_name: {disease_name}")
        if action == 'get_dinh_nghia':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"Định nghĩa của {disease.name}: {disease.definition}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_trieu_chung':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"Triệu chứng của {disease.name}: {disease.symptoms}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_phuong_phap':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"Phương pháp điều trị {disease.name}: {disease.treatment}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."

        elif action == 'get_nguyen_nhan':
            try:
                disease = Disease.objects.get(name__iexact=disease_name)
                fulfillment_text = f"Nguyên nhân của {disease.name}: {disease.cause}"
            except Disease.DoesNotExist:
                fulfillment_text = f"Không tìm thấy thông tin về bệnh {disease_name}."
                
        # Định dạng phản hồi cho Dialogflow
        response = {
            "fulfillmentText": fulfillment_text,
            "source": "webhook"
        }
        return Response(response, status=status.HTTP_200_OK)