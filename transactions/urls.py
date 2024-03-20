"""url patterns for the transactions app"""
from django.urls import path
from . import views

app_name = 'transactions'  # pylint: disable=invalid-name

urlpatterns = [
    path('cart', views.OrderListView.as_view(), name='cart'),
    path('history', views.TransactionListView.as_view(), name='history')
]
