"""base urls"""
from django.contrib import admin
from django.urls import path, include
from products import urls as products_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(products_urls)),
]
