"""views for the transactions app"""
from django.views.generic import ListView
from . import models

# Create your views here.


# region - buyer end

class OrderListView(ListView):
    """Cart page: display the uncomfirmed orders made by the user"""
    model = models.Order
    template_name = "cart.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(buyer=self.request.user, is_confirmed=False)

        return queryset
    



class TransactionListView(ListView):
    """Purchase history page: display the past transactions made by the user"""
    model = models.Transaction
    template_name = "purchase_history.html"

# endregion
