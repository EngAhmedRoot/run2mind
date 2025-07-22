from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from customusers.models import Customusers

class Patients(models.Model):

    Gender_Choices = [
        ('male', _('Male')),  # ذكر
        ('female', _('Female'))  # أنثى
    ]

    user = models.OneToOneField(Customusers, on_delete=models.CASCADE, related_name='patient_profile')
    file_no = models.SlugField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=500)
    job = models.CharField(max_length=250, null=True, blank=True)

    birthdate = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=6,null=False,choices=Gender_Choices,default='male',verbose_name=_('gender'))
    details = models.TextField(max_length=1000,null=True, blank=True)
    file = models.FileField(upload_to='patients/', null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='patients_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        db_table = "patients"
        verbose_name_plural = "Patients"
