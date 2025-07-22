# run2mind/views.py
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings

def switch_language(request):
    language = request.GET.get('language', 'en')
    next_url = request.GET.get('next', '/')
    
    if language not in ['en', 'ar']:
        language = 'en'

    response = redirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    translation.activate(language)
    return response
