from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os

from customusers.models import Customusers



class Experts(models.Model):
    Gender_Choices = [
        ('male', _('Male')),
        ('female', _('Female')),
    ]

    user = models.OneToOneField(Customusers, on_delete=models.CASCADE, related_name='expert_profile')
    name_ar = models.CharField(max_length=255, verbose_name=_('Name (Arabic)'))
    name_en = models.CharField(max_length=255, verbose_name=_('Name (English)'))

    birthdate = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=Gender_Choices, default='male', verbose_name=_('Gender'))
    experience_years = models.PositiveIntegerField(default=25, verbose_name=_('Years of Experience'))
    file = models.FileField(upload_to='experts/', null=True, blank=True)

    specialization_ar = models.CharField(max_length=255, verbose_name=_('Specialization (Arabic)'))
    specialization_en = models.CharField(max_length=255, verbose_name=_('Specialization (English)'))
    certificates_ar = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Certificates (Arabic)'))
    certificates_en = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Certificates (English)'))
    details_ar = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Details (Arabic)'))
    details_en = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Details (English)'))


    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experts_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='experts_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # حذف الملف القديم إذا تم رفع ملف جديد
        if self.pk:  # إذا كانت البيانات موجودة (تحديث وليس إضافة جديدة)
            old_file = Experts.objects.filter(pk=self.pk).first().file
            if old_file and self.file != old_file:  # إذا تغير الملف
                if os.path.isfile(old_file.path):  # تأكد من أن الملف موجود فعليًا
                    os.remove(old_file.path)  # حذف الملف القديم

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # حذف الملف عند حذف السجل
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"{self.name_en} - {self.specialization_en}"

    class Meta:
        db_table = "experts"
        verbose_name_plural = "Experts"

