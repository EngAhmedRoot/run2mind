"""run2mind URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static

from chatnests import consumers


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('auth/', include('social_django.urls', namespace='social')), 
    path('dashboard/', include('dashboard.urls')),
    path('customusers/', include('customusers.urls')),
    path('customgroups/', include('customgroups.urls')),
    path('customusergroup/', include('customusergroup.urls')),
    path('customgrouppermissions/', include('customgrouppermissions.urls')),
    path('experts/', include('experts.urls')),
    path('expertsessions/', include('expertsessions.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('sessionappointments/', include('sessionappointments.urls')),
    
    path('chatnests/', include('chatnests.urls')),
    path('chatbot/', include('chatbot.urls')),


    # WebSocket path
    re_path(r'ws/chat/(?P<room_name>chat_\d+_\d+)/$', consumers.ChatConsumer.as_asgi()),  
)


# Add static file serving for media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)