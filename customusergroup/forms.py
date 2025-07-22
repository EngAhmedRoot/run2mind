from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from customusers.models import Customusers

class CustomusergroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Group")  

    class Meta:
        model = Customusers
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username'), 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email'), 'readonly': 'readonly'}),
            'group': forms.Select(attrs={'class': 'form-control ', }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = _("---- Choose A Group ----")

        if 'instance' in kwargs:
            user = kwargs['instance']
            if user.groups.exists():
                self.fields['group'].initial = user.groups.first()
