from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import dialogflow
import os
import uuid

# Create your views here.
class DialogflowAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        project_id = 'newagent-qadf'
        
        # Get or create session_id for the user
        if 'dialogflow_session_id' not in request.session:
            request.session['dialogflow_session_id'] = str(uuid.uuid4())
        session_id = request.session['dialogflow_session_id']
        
        language_code = 'vi'
        
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        
        text_input = dialogflow.TextInput(text=user_message, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        
        response = session_client.detect_intent(session=session, query_input=query_input)
        
        fulfillment_text = response.query_result.fulfillment_text
        
        return Response({'message': fulfillment_text})
        
        
        
        