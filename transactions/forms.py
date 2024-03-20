"""forms for managing user input related to transactions"""
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """allow users to adjust the quantity, and apply discounts"""
    class Meta:  # pylint: disable=missing-class-docstring,too-few-public-methods
        model = Order
        fields = ['quantity', 'promo_code']
