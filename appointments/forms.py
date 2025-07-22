from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Appointments
from experts.models import Experts
from patients.models import Patients
from expertsessions.models import Expertsessions

class AppointmentsForm(forms.ModelForm):
    # تحديد الحقول الرئيسية لاختيار المريض، الخبير، الجلسة
    patient = forms.ModelChoiceField(
        queryset=Patients.objects.filter(user__is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Select Patient'),empty_label=None
    )
    expert = forms.ModelChoiceField(
        queryset=Experts.objects.none(),  # تصفية لاحقًا في `__init__`
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': True}),
        label=_('Select Expert'),empty_label=None
    )

    expertsession = forms.ModelChoiceField(
        queryset=Expertsessions.objects.none(),  # تصفية لاحقًا في `__init__`
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Select Expertsession'),empty_label=None
    )

    class Meta:
        model = Appointments
        fields = ['patient', 'expert', 'session_datetime', 'expertsession', 'status', 'notes']
        widgets = {
            'session_datetime': forms.DateInput(
                attrs={
                    'class': 'form-control flatpickr',
                    'type': 'date',
                    'placeholder': _('Session Date')
                }
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': _('Add any notes...'), 'rows': 5, 'style': 'resize: none;'}
            ),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user', None)  # المستخدم الحالي لتخصيص القائمة
        expert_id = kwargs.pop('expert_id', None)  # استخدم expert_id لتصفية الجلسات
        super().__init__(*args, **kwargs)

        # تخصيص القوائم بناءً على المستخدم الحالي
        if current_user:
            if current_user.user_type == 'expert':
                self.fields['expert'].queryset = Experts.objects.filter(user=current_user)
                self.fields['expert'].initial = Experts.objects.filter(user=current_user).first()
            elif current_user.user_type == 'patient':
                self.fields['patient'].queryset = Patients.objects.filter(user=current_user)
            else:
                self.fields['expert'].queryset = Experts.objects.all()
                self.fields['patient'].queryset = Patients.objects.filter(user__is_active=True)
        else:
            self.fields['expert'].queryset = Experts.objects.all()
            self.fields['patient'].queryset = Patients.objects.filter(user__is_active=True)


        # تصفية الجلسات بناءً على expert_id
        if expert_id:
            self.fields['expert'].queryset = Experts.objects.filter(id=expert_id)
            self.fields['expert'].initial = Experts.objects.filter(id=expert_id).first()
            self.fields['expertsession'].queryset = Expertsessions.objects.filter(expert_id=expert_id)
        else:
            self.fields['expertsession'].queryset = Expertsessions.objects.none()
    
        # تخصيص النصوص الافتراضية للحقل `price`
        #self.fields['price'].widget.attrs['readonly'] = True
