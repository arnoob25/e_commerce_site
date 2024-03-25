"""forms for saving user data"""
from django import forms
from django.contrib.auth import get_user_model
from . import models
from .models import MerchantInfo

User = get_user_model()


class BuyerSignUpForm(forms.ModelForm):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        model = User
        fields = ('username', 'email', 'password')


class MerchantSignUpForm(forms.ModelForm):  # pylint: disable=missing-class-docstring
    store_name = forms.CharField(max_length=100)

    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            MerchantInfo.objects.create(  # pylint: disable=no-member
                user=user, store_name=self.cleaned_data['store_name'])
        return user


class BuyerInfoForm(forms.ModelForm):
    """for saving user's address"""
    class Meta:  # pylint: disable=too-few-public-methods
        """specifying fields"""
        model = models.BuyerInfo
        fields = ['street_address', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['street_address'] = instance.street_address
            self.initial['city'] = instance.city
            self.initial['state'] = instance.state
            self.initial['zip_code'] = instance.zip_code

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['delivery_address'] = ', '.join([
            cleaned_data.get('street_address', ''),
            cleaned_data.get('city', ''),
            cleaned_data.get('state', ''),
            cleaned_data.get('zip_code', '')
        ])
        return cleaned_data
