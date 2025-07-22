from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from experts.models import Experts


class Languages(models.Model):
    LANGUAGE_CHOICES = [
        ('arabic', 'Arabic'),
        ('english', 'English'),
    ]
    language_code = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, unique=True)  

    def __str__(self):
        return f"{self.language_code}"


    class Meta:
        db_table = "languages"
        verbose_name = "Language"
        verbose_name_plural = "Languages"


class Sessiondurations(models.Model):
    DURATION_CHOICES = [
        (30, '30 minutes'),
        (60, '60 minutes'),
    ]
    
    duration = models.IntegerField(choices=DURATION_CHOICES, help_text="Duration in minutes")

    def __str__(self):
        return f"{self.duration} minutes"


    class Meta:
        db_table = "sessiondurations"
        verbose_name = "Sessionduration"
        verbose_name_plural = "Sessiondurations"


class Timeslots(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    class Meta:
        db_table = "timeslots"
        verbose_name = "Timeslot"
        verbose_name_plural = "Timeslots"


class Availabletimes(models.Model):
    day_of_week = models.CharField(max_length=9, choices=[
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday')
    ])
    timeslot = models.ForeignKey(Timeslots, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day_of_week} - {self.timeslot}"

    class Meta:
        db_table = "availabletimes"
        verbose_name = "Availabletime"
        verbose_name_plural = "Availabletimes"





# Create your models here.
class  Expertsessions(models.Model):

    expert = models.ForeignKey(Experts, on_delete=models.CASCADE, related_name='expert_session')
    session_price = models.DecimalField(max_digits=6, decimal_places=0, default=800)
    languages = models.ManyToManyField(Languages, related_name='expertsessions') 
    availabletimes = models.ManyToManyField(Availabletimes, related_name='Availabletimes')  
    sessionduration = models.ManyToManyField(Sessiondurations, related_name='Sessiondurations')  
    details = models.TextField(max_length=1000, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='expertsessions_created', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='expertsessions_updated', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)



    def __str__(self):
        return f"Session Info for {self.expert.name_en}"  

    class Meta:
        db_table = "expertsessions"
        verbose_name = "Expertsession"
        verbose_name_plural = "Expertsessions"