from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from customusers.models import Customusers



class Chatnests_chatroom(models.Model):
    ROOM_TYPE_CHOICES = (('private', 'Private'), ('group', 'Group'))
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='private')    
    room_name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Customusers, through='Chatnests_chatroom_participants')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatroom_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatroom_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', _('Active')), ('deactive', _('Deactive'))], default='active')  

    class Meta:
        db_table = 'chatnests_chatroom'

    def __str__(self):
        return f'{self.room_type} chatroom {self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # حفظ الكائن أولاً لضمان تعيين الـ id

        # إضافة المشاركين بعد الحفظ، عند التأكد من أن الـ id تم تعيينه
        if self.id:
            # هنا يمكنك إضافة المشاركين بعد أن يتم تعيين الـ id
            pass



class Chatnests_message(models.Model):
    sender = models.ForeignKey(Customusers, on_delete=models.CASCADE, related_name='sent_message')
    receiver = models.ForeignKey(Customusers, on_delete=models.CASCADE, related_name='received_message')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    delivery_status = models.CharField(
        max_length=20,
        choices=[('sent', 'Sent'), ('delivered', 'Delivered'), ('read', 'Read')],
        default='sent'
    )
    message_type = models.CharField(
        max_length=20,
        choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('file', 'File')],
        default='text'
    )
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('deactive', 'Deactive')], default='active')
    chatroom = models.ForeignKey(Chatnests_chatroom, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'chatnests_message'

    def __str__(self):
        return f'{self.sender} to {self.receiver}'











class Chatnests_chatroom_participants(models.Model):
    chatroom = models.ForeignKey(Chatnests_chatroom, on_delete=models.CASCADE) 
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    joined_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=10, choices=[('active', _('Active')), ('deactive', _('Deactive'))], default='active')  

    class Meta:
        db_table = 'chatnests_chatroom_participants'  
        unique_together = ('chatroom', 'participant')

    def __str__(self):
        return f'Participant {self.participant} in chatroom {self.chatroom}'




class Chatnests_chatpermission(models.Model):
    role_from = models.CharField(max_length=20, choices=[('expert', 'Expert'), ('patient', 'Patient')])
    role_to = models.CharField(max_length=20, choices=[('expert', 'Expert'), ('patient', 'Patient')])
    
    # Determines if the role can chat with the other
    can_chat = models.BooleanField(default=True) 
    
    # List of allowed message types for this role pair
    message_types_allowed = models.JSONField(default=list, help_text="List of allowed message types for this role pair (e.g., ['text', 'image']).")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatpermission_created', on_delete=models.SET_NULL, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatpermission_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=[('active', _('Active')), ('deactive', _('Deactive'))], default='active')

    class Meta:
        db_table = 'chatnests_chatpermission'

    def __str__(self):
        return f'{self.role_from} to {self.role_to}: {"Can chat" if self.can_chat else "Cannot chat"}'





class Chatnests_blocklist(models.Model):
    blocked_by = models.ForeignKey(Customusers, on_delete=models.CASCADE, related_name='blocking')
    blocked_user = models.ForeignKey(Customusers, on_delete=models.CASCADE, related_name='blocked')
    created_at = models.DateTimeField(auto_now_add=True)

