"""models for the user"""
from django.db import models
from django.contrib.auth import get_user_model
from configurations import DEFAULT_USER_TYPE, USER_TYPES


user_model = get_user_model()


class UserInfo(models.Model):
    """stores additional information about the user"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPES, default=DEFAULT_USER_TYPE
    )


class BuyerInfo(models.Model):
    """stores additional information on the buyer"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)


class MerchantInfo(models.Model):
    """stores additional information on the merchant"""
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    store_name = models.TextField()
