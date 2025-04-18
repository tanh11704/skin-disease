from django.urls import path
from .views import DialogflowWebhook

urlpatterns = [
    path('webhook/', DialogflowWebhook.as_view(), name='dialogflow-webhook'),
]