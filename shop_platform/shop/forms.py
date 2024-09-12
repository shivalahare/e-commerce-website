from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , Order

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'role', 'address', 'billing_address', 'shipping_address']



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity']  # Include fields that are relevant for order creation

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})