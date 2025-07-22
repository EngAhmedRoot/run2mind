from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Chatnests_chatroom


class ChatnestsAddForm(forms.ModelForm):

    class Meta:
        model = Chatnests_chatroom
        fields = '__all__'  # تشمل جميع الحقول في النموذج

        # تخصيص الأدوات لكل حقل
        widgets = {
            'participants': forms.SelectMultiple(attrs={'class': 'form-control basic'}),
            'status': forms.RadioSelect(attrs={'class': 'custom-control custom-radio custom-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # تخصيص حقل 'is_deleted' ليكون اختياريا ويكون افتراضيا 'active'
        self.fields['status'].required = False
        self.fields['status'].initial = 'active'

        # تخصيص Placeholder
        self.fields['participants'].widget.attrs.update({
            'placeholder': _('Select participants')
        })
