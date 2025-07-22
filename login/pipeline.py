from social_core.exceptions import AuthException

def custom_social_details(strategy, details, backend, *args, **kwargs):
    """
    خطوة لجلب تفاصيل المستخدم من مزود المصادقة الاجتماعية (مثل Google).
    """
    print(f"Custom Social Details: {details}")
    
    # إذا لم يكن البريد الإلكتروني موجودًا في التفاصيل، حاول الحصول عليه من الاستجابة
    if 'email' not in details:
        print("Email not found in details, checking response.")
        response = kwargs.get('response')
        if response and 'email' in response:
            details['email'] = response['email']
            print(f"Email found in response: {details['email']}")
        else:
            print("Email not found in response either.")
    
    return details

def custom_social_uid(strategy, details, backend, *args, **kwargs):
    """
    خطوة للحصول على معرف فريد للمستخدم من مزود المصادقة.
    """
    print(f"Custom Social UID: Using backend {backend.name}")
    
    # استخرج الـ UID من الاستجابة (response)
    response = kwargs.get('response')
    if response:
        uid = response.get('id')  # افترض أن الـ UID موجود في استجابة Google
        if uid:
            print(f"UID retrieved: {uid}")
            return {'uid': uid}  # ارجع الـ UID
        else:
            raise AuthException(backend, 'Unable to retrieve user UID')
    return {}

def custom_social_user(backend, user, response, *args, **kwargs):
    """دالة مخصصة لمعالجة uid إذا كانت مفقودة"""
    if not getattr(user, 'uid', None):
        uid = response.get('id')  # افترض أن الـ UID موجود في استجابة Google
        if uid:
            user.uid = uid
            user.save()
        else:
            raise AuthException(backend, 'Unable to retrieve user UID')
    return user

def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    خطوة لإنشاء مستخدم جديد إذا لم يكن موجودًا.
    """
    print(f"Custom Create User: User exists? {user is not None}")
    if user:
        return {'user': user}
    
    # تأكد من وجود البريد الإلكتروني في التفاصيل
    email = details.get('email')
    if not email:
        print("No email found in details.")
        raise AuthException(backend, 'Email is required to create a user')
    
    username = email.split('@')[0]  # تعيين اسم مستخدم افتراضي بناءً على البريد الإلكتروني
    print(f"Creating user: Username={username}, Email={email}")
    return {
        'user': strategy.create_user(
            username=username,
            email=email,
            first_name=details.get('first_name', ''),
            last_name=details.get('last_name', '')
        )
    }

def custom_user_details(strategy, details, backend, user=None, *args, **kwargs):
    """
    تحديث تفاصيل المستخدم إذا كان موجودًا.
    """
    print(f"Custom User Details: Updating user {user.username if user else 'None'}")
    if user:
        user.first_name = details.get('first_name', user.first_name)
        user.last_name = details.get('last_name', user.last_name)
        user.save()
        print(f"User updated: {user.username}")
    return {'user': user}

def custom_load_extra_data(strategy, details, response, user=None, *args, **kwargs):
    """
    تحميل بيانات إضافية من مزود المصادقة.
    """
    print(f"Response from Google: {response}")
    # تأكد من وجود البريد الإلكتروني
    if 'email' not in response:
        print("Email not found in response.")
    else:
        print(f"Email found in response: {response['email']}")
    return {'extra_data': response}

def debug_step(strategy, backend, details, *args, **kwargs):
    step_name = "Debug Step"
    print(f"Step: {step_name}, Backend: {backend.name}, Details: {details}")
    # لا تفعل شيئًا هنا سوى الطباعة
    return {}
