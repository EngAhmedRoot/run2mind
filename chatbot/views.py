import logging
import json 
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from .wit_ai_service import WitAiService
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  

logger = logging.getLogger(__name__)


#  عرض صفحة HTML الخاصة بالـ Chatbot
def chatbot_view(request):
    """عرض صفحة الدردشة HTML"""
    return render(request, 'chatbot/chatbot.html')

#  API لاستقبال الرسائل من الواجهة الأمامية
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"🚀 البيانات المستلمة: {data}")  # إضافة print هنا
            message = data.get('message', None)
            if message:
                response_data = {'message': 'تم استقبال الطلب بنجاح!', 'user_message': message}
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'error': 'يجب إرسال رسالة صالحة'}, status=400)
        except Exception as e:
            print(f"❌ خطأ: {e}")  # طباعة الخطأ للتتبع
            return JsonResponse({'error': 'حدث خطأ غير متوقع'}, status=500)



#  API لاستقبال الرسائل من الواجهة الأمامية وإرسالها إلى Wit.ai
class ChatbotAPIView(APIView):
    """API لاستقبال الرسائل من الواجهة الأمامية وإرسالها إلى Wit.ai"""
    
    def post(self, request, *args, **kwargs):
        """تستقبل الرسالة وتستدعي خدمة Wit.ai لمعالجتها"""
        
        serializer = MessageSerializer(data=request.data)
        
        if serializer.is_valid():
            message = serializer.validated_data['message']
            logger.info(f"📩 رسالة مستلمة من المستخدم: {message}")
            
            wit_ai_service = WitAiService()
            
            try:
                response = wit_ai_service.send_message(message)
                logger.info(f"🤖 رد Wit.ai: {response}")
                
                return Response({"reply": response}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"❌ خطأ أثناء الاتصال بـ Wit.ai: {str(e)}")
                
                return Response(
                    {"error": "حدث خطأ أثناء الاتصال بخادم Wit.ai. الرجاء المحاولة لاحقًا."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        logger.warning(f"⚠️ البيانات المرسلة غير صالحة: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
