from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.conf import settings

from expertsessions.models import Expertsessions  
from patients.models import Patients

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),         # قيد الانتظار
        ('confirmed', _('Confirmed')),    # مؤكد
        ('completed', _('Completed')),    # مكتمل
        ('cancelled', _('Cancelled')),    # ملغى
    ]

    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='sessions')
    expertsession = models.ForeignKey(Expertsessions, on_delete=models.CASCADE, verbose_name=_('Expertsessions')) 

    session_datetime = models.DateField(verbose_name=_('Session DateTime')) 
    meeting_link = models.URLField(max_length=500, null=True, blank=True) 
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))  
    notes = models.TextField(null=True, blank=True, verbose_name=_('Notes')) 

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "appointments"
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['session_datetime', 'patient', 'expertsession']


    
    def is_upcoming(self):
        """تشيك هل الجلسة لسه قدام ولا لا"""
        session_datetime = datetime.combine(self.session_datetime)
        return session_datetime > datetime.now()

    def __str__(self):
        return f"Session for {self.patient.name} with {self.expertsession.expert.name} on {self.session_datetime}"



