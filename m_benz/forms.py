from django import forms 
from . models import Car,CarImage

class CarForm(forms.ModelForm):
    
    class Meta:
        model = Car
        fields = ("name","description","year","price",
                  "color","drive_type","city","generation",
                  "car_body","engine_capacity","mileage","drivetrain",
                  "steering_wheel","quantity")
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название машины'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание авто',
                'rows': 4
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год выпуска'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цвет машины'
            }),
            "mileage": forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пробег машины'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Город"
            }),
            'car_body': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Кузов'
            }),
            'drivetrain': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Привод'
            }),
            "engine_capacity" : forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Объем двигателя'
            }),
            "steering_wheel": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Руль"
            }),
            'generation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Поколение машины'
            }),
            'drive_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Коробка передач"
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'forms-control',
                'placeholder': 'Количества машин'
            }),
        }
 