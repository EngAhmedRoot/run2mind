from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PatientsignupForm(forms.Form):
    name = forms.CharField(
        max_length=500, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')], 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
