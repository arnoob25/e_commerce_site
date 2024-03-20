"""views for the transactions app"""
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms


# region - buyer end


class OrderListView(LoginRequiredMixin, ListView): # TODO: ability to delete order 
    """Cart page: display the unconfirmed orders made by the user"""
    model = models.Order
    template_name = "cart.html"
    form_class = forms.OrderForm

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(buyer=self.request.user, is_confirmed=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_list = context['object_list']
        forms_with_instances = {order.id: self.form_class(
            instance=order) for order in order_list}
        context['forms'] = forms_with_instances
        return context

    def post(self, request, *args, **kwargs):
        """handles the buyer adjusting quantity and applying promo codes"""
        order_id = request.POST.get('order_id')

        order = models.Order.objects.get(  # pylint: disable=no-member
            id=order_id, buyer=request.user, is_confirmed=False)

        form = self.form_class(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('transactions:cart')

        return self.get(request, *args, **kwargs)


class TransactionListView(ListView):
    """Purchase history page: display the past transactions made by the user"""
    model = models.Transaction
    template_name = "purchase_history.html"


# endregion
