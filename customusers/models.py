from django.contrib.auth.models import AbstractUser
from django.db import models

class Customusers(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('expert', 'Expert'),
        ('patient', 'Patient'),
    )
    
    user_type = models.CharField(max_length=12, choices=USER_TYPE_CHOICES)

    file = models.FileField(upload_to='customuser/', null=True, blank=True)
    
    # Avoid conflicts with auth.User by setting a different related_name
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        db_table = "customusers"

    def __str__(self):
        return self.username
