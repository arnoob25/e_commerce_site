"""models for managing transactions"""
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

user_model = get_user_model()


class Order(models.Model):
    """manage buying requests, carts, wishlist, etc."""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    buyer = models.ForeignKey(user_model, on_delete=models.SET_NULL)
    seller = models.ForeignKey(user_model, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    is_promo_applied = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)


class Transaction(models.Model):
    """track deliveries, store transaction records, etc."""
    orders = models.ManyToManyField(Order)
    buyer = models.ForeignKey(user_model, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    total_amount = models.FloatField()
    transaction_method = models.TextField()
