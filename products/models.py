"""Models for creation and discovery of products"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
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
        slug (str): A slug for standard urls.
    """
    title = models.CharField(max_length=256)
    seller = models.ForeignKey(
        User, related_name='products', null=True, on_delete=models.SET_NULL,)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=PRODUCT_CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self):
        return f"Product: {self.title} - Category: {self.category} - Price: {self.price}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)


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
    image = models.ImageField(upload_to='media/product_images')

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
        if self.products:
            product_titles = ', '.join(
                product.title for product in self.products.all())  # pylint: disable=no-member
            return f"{self.title} at {self.discount}% off for: {product_titles}"
        return f"{self.title} at {self.discount}"
