# Generated by Django 5.2.4 on 2025-07-22 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatnests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chatnests_blocklist',
            name='blocked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocking', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_blocklist',
            name='blocked_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatpermission',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chatpermission_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatpermission',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chatpermission_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatroom',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chatroom_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatroom',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chatroom_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatroom_participants',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatnests.chatnests_chatroom'),
        ),
        migrations.AddField(
            model_name='chatnests_chatroom_participants',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_chatroom',
            name='participants',
            field=models.ManyToManyField(through='chatnests.Chatnests_chatroom_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_message',
            name='chatroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chatnests.chatnests_chatroom'),
        ),
        migrations.AddField(
            model_name='chatnests_message',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatnests_message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_message', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='chatnests_chatroom_participants',
            unique_together={('chatroom', 'participant')},
        ),
    ]
