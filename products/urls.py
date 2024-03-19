"""url patterns for the products app"""
from django.urls import path
from . import views

app_name = 'products'  # pylint: disable=invalid-name

urlpatterns = [
    path('', views.ProductListView.as_view(), name='discover'),
    path('product/<str:slug>/', views.ProductDetailView.as_view(), name='details'),
]
