from django import forms
from .models import Order


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['comments'].label = 'Комментарий'
        self.fields['buying_type'].label = 'Доставка'
        self.fields['address'].label = 'Адрес'

    class Meta:
        model = Order
        exclude = ('user', 'cart', 'status')


class RegisteredUserOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['comments'].label = 'Комментарий'
        self.fields['buying_type'].label = 'Доставка'
        self.fields['address'].label = 'Адрес'

    class Meta:
        model = Order
        fields = ('address', 'buying_type', 'comments')
