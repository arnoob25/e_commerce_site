"""models for managing wishlist, cart, checkout, sales analytics etc."""
from django.db import models
from django.utils import timezone
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
        unit_price (Decimal): The unit price of the product.
        quantity (PositiveInteger): The quantity of the product ordered.
        discount (PositiveInteger): The discount applied to the order.
        is_confirmed (Boolean): Whether the order is confirmed.
        payment_method (Text): The method of transaction.
        final_cost (Decimal): Final cost after accounting for quantity, and applying discount.
        promo_code (str): The promo code entered for the order.
    """
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    buyer = models.ForeignKey(
        user_model, null=True, on_delete=models.SET_NULL, related_name='buyer_orders')
    seller = models.ForeignKey(
        user_model, null=True, on_delete=models.SET_NULL, related_name='seller_orders')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(default=0)
    is_confirmed = models.BooleanField(default=False)
    final_cost = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD, blank=True)
    promo_code = models.CharField(max_length=20, blank=True)

    @property
    def calculate_cost(self):
        """Calculate the final cost after accounting for quantity, and applying discount."""
        discount_amount = (self.unit_price * self.discount) / 100
        discounted_price = self.unit_price - discount_amount
        return discounted_price * self.quantity

    @property
    def apply_discount(self):
        """Apply the highest discount offer, accounting the promo code and expiry."""
        offers = self.product.offers.filter(  # pylint: disable=no-member
            is_active=True)
        max_discount = 0
        applied_offer = None

        for offer in offers:
            if offer.expire_at and offer.expire_at < timezone.now():
                # Skip expired offers
                continue

            if offer.promo_code and offer.promo_code == self.promo_code:
                # user entered a promo code
                self.discount = offer.discount
                applied_offer = offer
                break

            if offer.discount > max_discount:
                max_discount = offer.discount
                applied_offer = offer

        if applied_offer:
            self.discount = applied_offer.discount

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price  # pylint: disable=no-member
        self.apply_discount  # pylint: disable=pointless-statement
        self.final_cost = self.calculate_cost
        super().save(*args, **kwargs)

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
