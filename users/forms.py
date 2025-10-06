from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name","email","password1","password2","phone_number")
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Имя пользователя'
            }),
            "first_name": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Имя"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        })
        
        
    