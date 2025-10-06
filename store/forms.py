from django import forms

class CheckoutForm(forms.Form):
    city = forms.CharField(widget=forms.TextInput, label="Город")
    street = forms.CharField(widget=forms.TextInput, label="Улица")
    house = forms.CharField(widget=forms.TextInput, label="Дом")
    
    payment_method = forms.ChoiceField(
        choices=[("cash", "Оплата при получении"),("card", "Онлайн-оплата")],
        label="Метод оплаты")
    comment = forms.CharField(widget=forms.Textarea
        (attrs={"class": "form-control","rows":3}), 
        label="Комментарий",
        required=False)
    
    