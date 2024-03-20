"""url patterns for the products app"""
from django.urls import path
from . import views

app_name = 'products'  # pylint: disable=invalid-name

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('product/<str:slug>', views.ProductDetailView.as_view(), name='details'),

    # merchant end

    path('m/store', views.MerchantProductListView.as_view(), name='m-list'),
    path('m/product/<str:slug>',
         views.MerchantProductDetailView.as_view(), name='m-details'
         ),
    path('m/product/create', views.MerchantProductCreateView.as_view(), name='m-create_product'),
    path('m/offer/create', views.MerchantOfferCreateView.as_view(), name='m-create_offer'),
]
