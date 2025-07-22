from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission

class GrouppermissionsForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(), 
        widget=forms.CheckboxSelectMultiple, 
        required=False,
        label=_('Permissions'),
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Group Name'),'readonly': 'readonly','style': 'color:#1f9f70;', }),
        }

    def __init__(self, *args, **kwargs):
        super(GrouppermissionsForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()
