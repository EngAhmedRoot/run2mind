from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserChangeForm
from .models import Customusers

class CustomusersChangeForm(UserChangeForm):
    IS_ACTIVE_CHOICES = (
        (True, _('Active')),
        (False, _('Deactive')),
    )

    is_active = forms.ChoiceField(
        choices=IS_ACTIVE_CHOICES,
        widget=forms.RadioSelect,
        label=_("Is Active")
    )

    user_group_message = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label=_("User Group Message")
    )

    class Meta:
        model = Customusers
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'is_active','file']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}),
            'user_type': forms.Select(attrs={'class': 'form-control basic'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('First Name')}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': _('File')}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # إزالة الحقول الخاصة بكلمات المرور عند تعديل المستخدم
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

        # إضافة الخيار الافتراضي إلى حقل user_type
        user_type_choices = [(None, _("---- Choose UserType ----"))] + [
            choice for choice in self.fields['user_type'].choices if choice[0]
        ]
        self.fields['user_type'].choices = user_type_choices

        # تخصيص queryset لحقل user_type بناءً على صلاحيات المستخدم الحالي
        if current_user and (current_user.is_superuser or current_user.is_staff):
            self.fields['user_type'].queryset = Customusers.objects.all()
        elif current_user and current_user.user_type == 'admin':
            self.fields['user_type'].queryset = Customusers.objects.all()
        else:
            self.fields['user_type'].queryset = Customusers.objects.filter(username=current_user.username)

        # إعداد الرسالة المبدئية
        if self.instance.pk and self.instance.user_type:
            self.fields['user_group_message'].initial = self.get_user_group_message(self.instance.user_type)

    def get_user_group_message(self, user_type):
        user_group_messages = {
            'admin': 'User in Admin-Group',
            'expert': 'User in Expert-Group',
            'receptionist': 'User in Receptionist-Group',
            'patient': 'User in Patient-Group',
            'user': 'User in User-Group',
        }
        return user_group_messages.get(user_type, '')



    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Customusers.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(_('A user with that username already exists.'))
        return username





class ChangePasswordForm(UserChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Old Password')}),
        label=_('Old Password')
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('New Password')}),
        label=_('New Password')
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm New Password')}),
        label=_('Confirm New Password')
    )

    class Meta:
        model = Customusers
        fields = ['old_password', 'password1', 'password2', 'user_type']
        widgets = {
            'old_password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Old Password')}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('New Password')}),
            'password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Confirm Password')}),
            'user_type': forms.HiddenInput(attrs={'class': 'form-control basic'}),
        }

    def __init__(self, *args, **kwargs):
        # تعيين المستخدم الحالي كخاصية
        self.user = kwargs.pop('user', None)  # استخراج المستخدم الحالي
        super().__init__(*args, **kwargs)

        user_type_choices =  [
            choice for choice in self.fields['user_type'].choices if choice[0]
        ]
        self.fields['user_type'].choices = user_type_choices


        # تخصيص queryset لحقل user_type بناءً على صلاحيات المستخدم الحالي
        if self.user and (self.user.is_superuser or self.user.is_staff):
            self.fields['user_type'].queryset = Customusers.objects.all()
        elif self.user and self.user.user_type == 'admin':
            self.fields['user_type'].queryset = Customusers.objects.all()
        else:
            self.fields['user_type'].queryset = Customusers.objects.filter(username=self.user.username)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        # التحقق من كلمة المرور القديمة باستخدام self.user
        if self.user and not self.user.check_password(old_password):
            raise ValidationError(_('The old password is incorrect.'))
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError(_('The two new passwords do not match.'))

        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        # تحديث كلمة المرور للمستخدم الحالي
        if self.user:
            self.user.set_password(password)
            if commit:
                self.user.save()
        return self.user
