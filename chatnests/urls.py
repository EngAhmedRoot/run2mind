from django.urls import path
from .views import ( ChatnestsMessagesView,SendMessageView)

app_name = 'chatnests'

urlpatterns = [
    path('send_message/<int:receiver_id>/', SendMessageView.as_view(), name='send_message'),

    path('chatnests_messages/', ChatnestsMessagesView.as_view(), name='chatnests_messages'),
    path('chatnests_messages/<int:receiver_id>/', ChatnestsMessagesView.as_view(), name='chatnests_message_with_receiver'),
    path('send_message/<int:receiver_id>/', SendMessageView.as_view(), name='send_message'),


]