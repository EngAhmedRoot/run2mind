from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.shortcuts import  render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Max, Q


from django.views import View


from .forms import ChatnestsAddForm
from .models import Chatnests_chatroom, Chatnests_message, Chatnests_chatroom_participants
from django.contrib.auth.models import User
from experts.models import Experts  
from .models import Chatnests_chatroom, Customusers



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from django.shortcuts import render
from django.contrib import messages
from .models import Chatnests_message


from django.db import transaction
from django.http import JsonResponse


from django.views.generic.edit import CreateView
from .models import Chatnests_message, Chatnests_chatroom, Customusers




class ChatnestsMessagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # جلب جميع غرف الدردشة الخاصة بالمستخدم الذي قام بتسجيل الدخول
        chatrooms = Chatnests_chatroom.objects.filter(
            room_type='private',
            participants=request.user
        ).prefetch_related('participants', 'chatnests_message_set')

        # استخراج آخر رسالة لكل غرفة دردشة
        latest_messages = []
        for chatroom in chatrooms:
            latest_message = Chatnests_message.objects.filter(
                chatroom=chatroom
            ).order_by('-timestamp').first()

            if latest_message:
                latest_messages.append({
                    'chatroom': chatroom,
                    'latest_message': latest_message,
                })

        # تجهيز الرسائل وعرضها في القالب
        messages_data = []
        for data in latest_messages:
            chatroom = data['chatroom']
            latest_message = data['latest_message']

            #currentuser  
            sender = latest_message.sender
            receiver = latest_message.receiver

            #otherparty_user 
            other_party = receiver if sender == request.user else sender
            print(latest_message.is_read)

            # جلب صورة الـ Expert إذا كان الطرف الآخر هو expert
            other_party_avatar = None
            if other_party.user_type == 'expert' and hasattr(other_party, 'expert_profile'):
                expert = other_party.expert_profile
                other_party_avatar = expert.file if expert.file else None

            
            messages_data.append({
                'room_id': chatroom.id,  # إضافة room_id
                'room_name': chatroom.room_name,
                'otherparty_id': other_party.id,
                'otherparty_name': other_party.get_full_name() or other_party.username,
                'otherparty_avatar': other_party_avatar,  # صورة الطرف الآخر
                'content': latest_message.content,  # محتوى آخر رسالة
                'is_read': latest_message.is_read,
                'timestamp': latest_message.timestamp,
                'room_name_display': f"Room: {chatroom.room_name}",  # اسم الغرفة
            })

        return render(request, 'chatnests/chatnests_messages.html', {'messages': messages_data})



    def post(self, request, *args, **kwargs):
        #print(f"Logged in user: {request.user.id}")
        room_id = request.POST.get('room_id')  # جلب room_id من الطلب
        user = request.user
        currentuser_id = request.user.id
        sender_name=''
        otherparty_avatar=''


        if room_id:
            try:
                # التأكد من أن الغرفة موجودة وأن المستخدم مشارك فيها
                chatroom = Chatnests_chatroom.objects.prefetch_related('participants').get(id=room_id)
                print(chatroom)
                otherparty_user = chatroom.participants.exclude(id=user.id).first()
                print(otherparty_user)
                if otherparty_user is None:
                    otherparty_user = user

                # تحديث جميع الرسائل في الغرفة إلى is_read=True
                Chatnests_message.objects.filter(chatroom=chatroom,   is_read=False).update(is_read=True)
                # جلب جميع الرسائل في الغرفة
                messages = Chatnests_message.objects.filter(chatroom=chatroom).order_by('timestamp')

                messages_data = []
                last_date = None

                for message in messages:
                    message_date = message.timestamp.strftime('%Y-%m-%d')

                    sender_avatar = '/assets/run2mind/images/profile_image.jpg'  # القيمة الافتراضية

                    if message.sender.user_type == 'expert' and hasattr(message.sender, 'expert_profile'):
                        expert = message.sender.expert_profile
                        if expert.file:
                            sender_avatar = expert.file.url
                    elif message.sender.user_type == 'patient' and hasattr(message.sender, 'patient_profile'):
                        patient = message.sender.patient_profile
                        if patient.file:
                            sender_avatar = patient.file.url



                    messages_data.append({
                        'otherparty_id': message.sender.id,
                        'currentuser_id': currentuser_id,
                        'sender_name': message.sender.get_full_name() or message.sender.username,
                        'otherparty_avatar': sender_avatar,
                        'message_content': message.content,
                        'timestamp': message.timestamp,
                        'last_date': last_date,  # آخر تاريخ تمت معالجته
                    })

                    last_date = message_date  # تحديث التاريخ للرسالة التالية


                #print(messages_data)
                #print(f"Current User ID: {currentuser_id}")
                #print(f"Current otherparty_name: {sender_name}")
                #print(f"Current otherparty_name: {otherparty_avatar}")
                #print(f"Other Party User ID: {otherparty_user.id if otherparty_user else 'None'}")
                #print(f"Room ID: {room_id}")
                #print(messages_data)
                # تجهيز الرسائل للتصميم (HTML)
                html = render_to_string(
                    'chatnests/_chatnests_messages_partial.html',
                    {'messages_private_room': messages_data, 'request': request, 'otherparty_user': otherparty_user,'room_id':room_id}
                )

                # حساب عدد الرسائل
                message_count = messages.count()

                return JsonResponse({
                    'html': html,
                    'message_count': message_count,
                })

            except Chatnests_chatroom.DoesNotExist:
                return JsonResponse({'error': 'Room not found or you are not a participant.'}, status=404)

        return JsonResponse({'error': 'Invalid room_id.'}, status=400)












class SendMessageView(LoginRequiredMixin, CreateView):
    model = Chatnests_message
    fields = ['content']
    template_name = 'chatnests/send_message.html'

    def dispatch(self, request, *args, **kwargs):
        self.receiver_id = self.kwargs.get('receiver_id')
        self.receiver = get_object_or_404(Customusers, id=self.receiver_id)
    
        # جلب الاسم حسب البروفايل المتاح
        self.receiver_name_ar = None
        self.receiver_name_en = None
    
        if hasattr(self.receiver, 'expert_profile'):
            self.receiver_name_ar = self.receiver.expert_profile.name_ar
            self.receiver_name_en = self.receiver.expert_profile.name_en
        elif hasattr(self.receiver, 'patient_profile'):
            self.receiver_name_ar = self.receiver.patient_profile.name
            self.receiver_name_en = self.receiver.patient_profile.name  # مفيش إنجليزي هنا، فهنكرر الاسم
    
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver_name_ar'] = self.receiver_name_ar
        context['receiver_name_en'] = self.receiver_name_en
        return context

    def form_valid(self, form):
        sender = self.request.user
        receiver = self.receiver

        form.instance.sender = sender
        form.instance.receiver = receiver

        room_name = f"{min(sender.id, receiver.id)}_{max(sender.id, receiver.id)}"

        chatroom, created = Chatnests_chatroom.objects.get_or_create(
            room_name=room_name,
            room_type='private'
        )

        if created:
            chatroom.save()

        chatroom.participants.add(sender, receiver)
        form.instance.chatroom = chatroom

        with transaction.atomic():
            self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Message sent successfully!'}, status=200)

        return super().form_valid(form)





# إنشاء غرفة دردشة خاصة
# دالة إنشاء غرفة دردشة خاصة بين مريض وطبيب
def create_private_room(sender, receiver):
    """
    إنشاء غرفة دردشة خاصة بين طبيب ومريض.
    """
    if sender.user_type == 'expert' and receiver.user_type == 'patient':
        # تحقق من وجود غرفة دردشة بين نفس الطبيب والمريض
        existing_room = Chatnests_chatroom.objects.filter(
            room_type='private',
            participants=sender
        ).filter(participants=receiver).first()  # استخدم Filter بدلاً من '=' هنا

        if existing_room:
            return existing_room  # إرجاع الغرفة إذا كانت موجودة بالفعل

        # إنشاء غرفة جديدة
        room = Chatnests_chatroom.objects.create(
            room_type='private',
            created_by=sender
        )
        room.participants.add(sender, receiver)  # إضافة المشاركين إلى الغرفة
        return room
    else:
        # رفض العملية إذا لم تكن بين طبيب ومريض
        raise ValidationError("Private rooms can only be created between a expert and a patient.")



# عرض لإنشاء غرفة دردشة خاصة
class CreatePrivateChatroomView(LoginRequiredMixin, View):
    """
    يعالج عملية إنشاء غرفة دردشة خاصة بين المستخدم الحالي وشخص آخر.
    """
    def get(self, request, *args, **kwargs):
        receiver_id = kwargs.get('receiver_id')
        receiver = get_object_or_404(Customusers, id=receiver_id)
        available_users = Customusers.objects.filter(user_type='patient')
    
        print(f"Receiver: {receiver}, Available Users: {available_users}")  # Debugging
        return render(request, 'chatnests/create_private_chatroom.html', {
        'receiver': receiver,
        'available_users': available_users
    })


    def post(self, request, *args, **kwargs):
        receiver_id = kwargs.get('receiver_id')  # جلب معرف المستقبل
        receiver = get_object_or_404(Customusers, id=receiver_id)  # جلب المستخدم المستقبل

        try:
            # إنشاء الغرفة الخاصة
            room = create_private_room(request.user, receiver)
            messages.success(request, "Private chatroom created successfully!")
            return redirect('chatnests:chat_room', room_name=room.id)
        except ValidationError as e:
            # رسالة خطأ عند وجود مشكلة
            messages.error(request, str(e))
            return redirect('chatnests:list')









# إنشاء غرفة دردشة جماعية
def create_group_chatroom(admin, participants):
    """
    إنشاء غرفة دردشة جماعية تشمل فقط الأطباء.
    """
    if all(participant.user_type == 'expert' for participant in participants):
        room = Chatnests_chatroom.objects.create(
            room_type='group',
            created_by=admin,
        )
        room.participants.set(participants)  # تعيين المشاركين
        return room
    else:
        raise ValidationError(_("Group rooms can only include experts."))





# عرض لإنشاء غرفة دردشة جماعية
class CreateGroupChatroomView(LoginRequiredMixin, View):
    """
    يعالج عملية إنشاء غرفة دردشة جماعية.
    """
    def post(self, request, *args, **kwargs):
        participant_ids = request.POST.getlist('participants')  # جلب المعرفات من POST
        participants = User.objects.filter(id__in=participant_ids)  # جلب المستخدمين المشاركين
        admin = request.user  # المستخدم الحالي كمسؤول الغرفة

        try:
            # إنشاء الغرفة الجماعية
            room = create_group_chatroom(admin, participants)
            messages.success(request, _("Group chatroom created successfully!"))
            return redirect('chatnests:chat_room', room_name=room.id)
        except ValidationError as e:
            # رسالة خطأ عند وجود مشكلة
            messages.error(request, str(e))
            return redirect('chatnests:list')
