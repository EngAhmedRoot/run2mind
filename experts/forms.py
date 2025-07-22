from django import forms
from django.utils.translation import gettext_lazy as _
import datetime

from .models import Experts
from customusers.models import Customusers 

class ExpertsForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=Customusers.objects.filter(user_type='expert', is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Select Expert User'),
        empty_label=_("--- Choose User ---")
    )


    class Meta:
        model = Experts
        fields = '__all__'

        widgets = {
            'name_ar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Expert NameAR')}),
            'name_en': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Expert NameEN')}),

            'specialization_ar': forms.TextInput(attrs={'class': 'form-control','placeholder': _('SpecializationAR')}),
            'specialization_en': forms.TextInput(attrs={'class': 'form-control','placeholder': _('SpecializationEN')}),

            'birthdate': forms.DateInput(attrs={'class': 'form-control flatpickr','type': 'date',
                    'placeholder': _('Birthdate'), 'onblur': 'this.type="date"', 'onfocus': 'this.type="date"'}),

            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone')}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Mobile')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email'), 'readonly': 'readonly'}),
            'gender': forms.RadioSelect(attrs={'class': 'custom-control custom-radio custom-control'}),

            'details_ar': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('DetailsAR'), 'rows': 5,'style': 'resize: none; overflow: auto;'}),
            'details_en': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('DetailsEN'), 'rows': 5,'style': 'resize: none; overflow: auto;'}),

            'is_deleted': forms.RadioSelect(attrs={'class': 'custom-control custom-radio custom-control'})
        }



    def __init__(self, *args, **kwargs):
        #get current user from view
        current_user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        if current_user and current_user.user_type == 'expert':
            self.fields['user'].queryset = Customusers.objects.filter(id=current_user.id, is_active=True)
        elif  current_user and current_user.user_type == 'patient':
            self.fields['user'].queryset = Customusers.objects.none()
        elif  current_user and current_user.user_type == 'user':
            self.fields['user'].queryset = Customusers.objects.none()
        else:
            self.fields['user'].queryset = Customusers.objects.filter(user_type='expert', is_active=True)




