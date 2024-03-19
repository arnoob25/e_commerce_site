"""Models for creation and discovery of products"""
from django.db import models
from django.contrib.auth import get_user_model
from configurations import PRODUCT_CATEGORIES

User = get_user_model()


class Product(models.Model):
    """
    Model representing a product.

    Attributes:
        title (str): The title of the product.
        seller (User): The user selling the product.
        description (str): A description of the product.
        category (str): The category the product belongs to.
        price (float): The price of the product.
        stock (int): The number of units in stock.
    """
    title = models.CharField(max_length=256)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    category = models.CharField(max_length=100, choices=PRODUCT_CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()  #

    def __str__(self):
        return f"Product: {self.title} - Category: {self.category} - Price: {self.price}"


class ProductImage(models.Model):
    """
    Model representing an image for a product.

    Attributes:
        product (Product): The product the image belongs to.
        caption (str): A caption for the image.
        image (ImageField): The image file.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    caption = models.TextField(blank=True)  # Caption is optional
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"Image {self.pk} for {self.product.title}"  # pylint: disable=no-member


class Offer(models.Model):
    """
    Model representing an offer for a product.

    Attributes:
        title (str): The title of the offer.
        products (QuerySet): The products the offer is for.
        discount (int): The percentage discount for the offer.
        promo_code (str): The promo code for the offer.
    """
    title = models.CharField(max_length=100)
    products = models.ManyToManyField(
        Product, related_name='offers'
    )
    discount = models.PositiveIntegerField()
    promo_code = models.CharField(max_length=20, unique=True, blank=True)

    def __str__(self):
        product_titles = ', '.join(
            product.title for product in self.products.all())  # pylint: disable=no-member
        return f"{self.title} at {self.discount}% off for: {product_titles}"
