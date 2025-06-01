from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.validators import ValidationError
from datetime import date
from django.contrib.auth.forms import UserChangeForm
from pytz import common_timezones

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(
        label="Телефон",
        required=False,
        help_text="Формат: +375 (XX) XXX-XX-XX",
        widget=forms.TextInput(attrs={'placeholder': '+375 (XX) XXX-XX-XX'})
    )
    
    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'phone', 
            'date_of_birth',
            'password1', 
            'password2'
        ]

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < 18:
            raise forms.ValidationError("Вам должно быть не менее 18 лет для регистрации")
        return dob

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин или Email",
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class ProfileEditForm(UserChangeForm):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in common_timezones],
        label="Часовой пояс"
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата рождения",
        input_formats=['%d/%m/%Y', '%Y-%m-%d']
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'timezone', 'date_of_birth']
        labels = {
            'phone': 'Телефон'
        }

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance
        user.date_of_birth = cleaned_data.get('date_of_birth')
        
        try:
            user.clean() 
        except ValidationError as e:
            self.add_error('date_of_birth', e)
        
        return cleaned_data