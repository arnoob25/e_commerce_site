"""models for creation and discovery of products"""
from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class Product(models.Model):
    """information on the product"""
    title = models.CharField(max_length=256, required=True)
    seller = models.ForeignKey(user_model, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()  # amount of units in stock


class ProductImage(models.Model):
    """image for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField()

    class Meta:
        """meta information for the model"""
        unique_together = (('product', 'image'),) # Enforces unique combination of product and image


class Offer(models.Model):
    """manage offers"""
    title = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    discount = models.IntegerField()  # percentage
    promo_code = models.TextField()
