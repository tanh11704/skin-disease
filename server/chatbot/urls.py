from django.urls import path
from .views import DialogflowAPIView

urlpatterns = [
    path('dialogflow/', DialogflowAPIView.as_view(), name='dialogflow'),
]