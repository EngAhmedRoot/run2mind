from channels.generic.websocket import AsyncWebsocketConsumer
import json
from chatnests.models import Chatnests_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # الحصول على اسم الغرفة من URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # الانضمام إلى مجموعة الغرفة
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # قبول الاتصال
        await self.accept()

    async def disconnect(self, close_code):
        # مغادرة مجموعة الغرفة
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # تلقي البيانات من الـ WebSocket
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message_content']
        sender_id = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']

        # حفظ الرسالة في قاعدة البيانات
        message = Chatnests_Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_content=message_content
        )

        # إرسال الرسالة إلى WebSocket لجميع المتصلين في نفس الغرفة
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_content': message_content,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )

    async def chat_message(self, event):
        # تلقي الرسالة من الـ group_send
        message_content = event['message_content']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']

        # إرسال الرسالة إلى WebSocket
        await self.send(text_data=json.dumps({
            'message_content': message_content,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))
