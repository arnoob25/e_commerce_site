"""views for the transactions app"""
from django.views.generic import ListView
from . import models

# Create your views here.


# region - buyer end

class OrderListView(ListView):
    """Cart page: display the uncomfirmed orders made by the user"""
    model = models.Order
    template_name = "cart.html"


class TransactionListView(ListView):
    """Purchase history page: display the past transactions made by the user"""
    model = models.Transaction
    template_name = "purchase_history.html"

# endregion
