from django.urls import path
from .views import chatbot_view, chatbot_api, ChatbotAPIView

urlpatterns = [
    path('', chatbot_view, name='chatbot_view'), 
    path('api/simple/', chatbot_api, name='chatbot_api'),  
    path('api/', ChatbotAPIView.as_view(), name='chatbot_api_view'),  
]