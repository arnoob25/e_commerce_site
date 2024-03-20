"""models for managing wishlist, cart, checkout, sales analytics etc."""
from django.db import models
from django.contrib.auth import get_user_model
from configurations import PAYMENT_METHOD
from products.models import Product

user_model = get_user_model()


class Order(models.Model):
    """
    Model representing an order made by a user.

    Attributes:
        product (Product): The product ordered.
        buyer (User): The user who made the order.
        seller (User): The user selling the product.
        price (Decimal): The price of the product.
        quantity (PositiveInteger): The quantity of the product ordered.
        discount (PositiveInteger): The discount applied to the order.
        is_confirmed (Boolean): Whether the order is confirmed.
        transaction_method (Text): The method of transaction.
    """
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    buyer = models.ForeignKey(
        user_model, null=True, on_delete=models.SET_NULL, related_name='buyer_orders')
    seller = models.ForeignKey(
        user_model, null=True, on_delete=models.SET_NULL, related_name='seller_orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(default=0)
    is_confirmed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, blank=True)

    def __str__(self):
        return f"Order {self.pk} for {self.product.title}"  # pylint: disable=no-member


class Transaction(models.Model):
    """
    Model representing a transaction made by a user.

    Attributes:
        orders (Order): The orders included in the transaction.
        buyer (User): The user who made the transaction.
        created_at (DateTime): The time the transaction was made.
        total_amount (Float): The total amount of the transaction.
        transaction_method (Text): The method of transaction.
    """
    orders = models.ManyToManyField(Order)
    buyer = models.ForeignKey(
        user_model, on_delete=models.CASCADE, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)

    def __str__(self):
        return f"Transaction {self.pk} by {self.buyer.username}"  # pylint: disable=no-member
