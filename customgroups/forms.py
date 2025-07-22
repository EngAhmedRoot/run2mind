from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class GroupsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name'] 

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': _('Group Name')
            }),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')  
        super(GroupsForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Group.objects.exclude(pk=self.instance.pk).filter(name=name).exists():
            raise forms.ValidationError(_("A group with this name already exists."))
        return name