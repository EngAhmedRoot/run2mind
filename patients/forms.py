
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Patients
from customusers.models import Customusers 

class PatientsForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=Customusers.objects.filter(user_type='patient', is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Select Doctor User'),
        empty_label=_("--- Choose User ---")
    )


    class Meta:
        model = Patients
        fields = '__all__'


        widgets = {
            'file_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient FileNo'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Patient Name')}),
            'job': forms.TextInput(attrs={'class': 'form-control',
                                                     'placeholder': _('Job')}),

            'birthdate': forms.DateInput(attrs={'class': 'form-control flatpickr','type': 'date',
                    'placeholder': _('Birthdate'), 'onblur': 'this.type="date"', 'onfocus': 'this.type="date"'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone')}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Mobile')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
            'gender': forms.RadioSelect(attrs={'class': 'custom-control custom-radio custom-control'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Details'), 'rows': 5,'style': 'resize: none; overflow: auto;'}),
            'is_deleted': forms.RadioSelect(attrs={'class': 'custom-control custom-radio custom-control'})
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        if 'instance' in kwargs and kwargs['instance']:
            instance = kwargs['instance']





