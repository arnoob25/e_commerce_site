"""views for the transactions app"""
from django.views.generic import ListView
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from user_management import models, forms
from user_management.forms import BuyerInfoForm
from . import models, forms


# region - buyer end


class OrderListView(LoginRequiredMixin, ListView):
    # pylint: disable=too-many-ancestors
    """Cart page: display the unconfirmed orders made by the user"""
    model = models.Order
    template_name = "cart.html"
    form_class = forms.OrderForm
    buyer_info_form_class = BuyerInfoForm
    payment_form_class = forms.TransactionForm

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
        context['subtotal'] = sum(order.final_cost for order in order_list)

        # Get the buyer's address information
        try:
            buyer_info = models.BuyerInfo.objects.get(  # pylint: disable=no-member
                user=self.request.user)
            context['buyer_info_form'] = self.buyer_info_form_class(
                instance=buyer_info)
        except models.BuyerInfo.DoesNotExist:  # pylint: disable=no-member
            context['buyer_info_form'] = self.buyer_info_form_class()

        # Add an empty payment form
        context['payment_form'] = self.payment_form_class()

        return context

    def post(self, request, *args, **kwargs):
        """handles the buyer adjusting quantity, applying promo codes, and placing the order"""
        order_id = request.POST.get('order_id')
        delete_order = request.POST.get('delete_order')

        if delete_order:
            # Handle order deletion
            order = get_object_or_404(
                models.Order, id=order_id, buyer=request.user, is_confirmed=False)
            order.delete()
            return redirect(reverse('transactions:cart'))

        if order_id:
            # Handle order update
            order = models.Order.objects.get(  # pylint: disable=no-member
                id=order_id, buyer=request.user, is_confirmed=False
            )
            form = self.form_class(request.POST, instance=order)
            if form.is_valid():
                # Update the existing order object
                for field, value in form.cleaned_data.items():
                    setattr(order, field, value)
                order.save()
            return redirect(reverse('transactions:cart'))

        payment_form = self.payment_form_class(request.POST)
        buyer_info_form = self.buyer_info_form_class(request.POST)

        # Check if the form submission is for the checkout form
        if 'checkout' in request.POST:
            if payment_form.is_valid() and buyer_info_form.is_valid():
                # Update or create buyer_info object
                buyer_info, is_created = models.BuyerInfo.objects.get_or_create(  # pylint: disable=no-member
                    user=request.user, defaults=buyer_info_form.cleaned_data)
                if not is_created:
                    for field, value in buyer_info_form.cleaned_data.items():
                        setattr(buyer_info, field, value)
                    buyer_info.save()

                orders = models.Order.objects.filter(  # pylint: disable=no-member
                    buyer=request.user, is_confirmed=False)
                total_amount = sum(order.final_cost for order in orders)
                payment_method = payment_form.cleaned_data['payment_method']
                transaction = models.Transaction.objects.create(  # pylint: disable=no-member
                    buyer=request.user,
                    total_amount=total_amount,
                    payment_method=payment_method,
                    delivery_address=buyer_info_form.cleaned_data['delivery_address']
                )
                transaction.orders.set(orders)

                # Update orders as confirmed
                orders.update(is_confirmed=True)
                return redirect(reverse('products:list'))

        return self.get(request, *args, **kwargs)


class TransactionListView(ListView):
    """Purchase history page: display the past transactions made by the user"""
    model = models.Transaction
    template_name = "purchase_history.html"


# endregion
