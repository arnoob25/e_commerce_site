"""adming config"""
from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductImage)


class OfferAdmin(admin.ModelAdmin):
    """allow selecting multiple products"""
    filter_horizontal = ('products',)


admin.site.register(models.Offer, OfferAdmin)
