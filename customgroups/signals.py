from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'customgroups':  
        groups = [
            'Admin-Group',
            'Expert-Group',
            'Patient-Group'
        ]

        for group_name in groups:
            Group.objects.get_or_create(name=group_name)
