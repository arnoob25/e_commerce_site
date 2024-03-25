"""forms for managing user input related to transactions"""
from django import forms
from . import models


class OrderForm(forms.ModelForm):
    """allow users to adjust the quantity, and apply discounts"""
    class Meta:  # pylint: disable=missing-class-docstring,too-few-public-methods
        model = models.Order
        fields = ['quantity', 'promo_code']

class TransactionForm(forms.ModelForm):
    """Form definition for Transaction."""
    class Meta:
        """Meta definition for Transactionform."""

        model = models.Transaction
        fields = ['payment_method']
