import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class WitAiService:

    def __init__(self):
        self.api_key = getattr(settings, 'WIT_AI_API_KEY', None)
        
        if not self.api_key:
            logger.error("⚠️ لم يتم العثور على WIT_AI_API_KEY في الإعدادات.")
        
        self.endpoint = settings.WIT_AI_SETTINGS.get('ENDPOINT', 'https://api.wit.ai/')
        self.api_version = settings.WIT_AI_SETTINGS.get('API_VERSION', '20241208')

    def send_message(self, message):
        url = f"{self.endpoint}message"
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'Content-Type': 'application/json'
        }
        params = {
            'v': self.api_version,  # إصدار الـ API
            'q': message  # الرسالة المرسلة من المستخدم
        }

        try:
            print(f"🔍 إرسال الرسالة إلى Wit.ai: {message}")
            response = requests.get(url, headers=headers, params=params, timeout=10)  # مهلة 10 ثواني
            print(f"🔍 الرد من Wit.ai: {response.status_code} - {response.text}")  # طباعة حالة الرد
            response.raise_for_status()  # إثارة استثناء إذا فشل الطلب
        
            response_data = response.json()

            if 'entities' not in response_data:  # تحقق من أن الرد يحتوي على كلمة "entities"
                print(f"⚠️ الرد من Wit.ai لا يحتوي على الكلمة المطلوبة: {response_data}")
        
            print(f"🤖 رد Wit.ai: {response_data}")
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ أثناء الاتصال بـ Wit.ai: {e}")  # طباعة الخطأ
            return {"error": "حدث خطأ أثناء الاتصال بـ Wit.ai", "details": str(e)}  # إعادة خطأ أوضح
