"""views for browsing, and offering products"""
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from configurations import PRODUCT_CATEGORIES
from transactions.models import Order
from . import models


# region - buyer end


class ProductListView(ListView):
    """view for the buyers to browse products by categories"""
    model = models.Product
    template_name = "discover_products.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')

        if category and category != 'all':
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PRODUCT_CATEGORIES

        return context


class ProductDetailView(LoginRequiredMixin, DetailView): # pylint: disable=too-many-ancestors
    """Allow buyers to view the product's specifications and make an order"""
    model = models.Product
    template_name = "product_details.html"

    def post(self, request, *args, **kwargs):
        """handle 'add to cart' and 'buy now' requests"""
        product = self.get_object()
        action = request.POST.get('action')

        if action in ['add_to_cart', 'buy_now']:
            Order.objects.create(  # pylint: disable=no-member
                product=product,
                buyer=request.user,
                seller=product.seller,
            )

            if action == 'buy_now':
                return redirect('transactions:cart')

            messages.success(
                request, f"{product.title} has been added to your cart.")

        return self.get(request, *args, **kwargs)


# endregion

# region - merchant end


class MerchantProductListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    """Display all the merchant's active products"""
    model = models.Product
    template_name = "m-store.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(seller=self.request.user)


class MerchantProductDetailView(DetailView):
    """Allow the merchant to view and edit the specifications of the product"""
    model = models.Product
    template_name = "m-product_details.html"


ProductImageFormSet = modelformset_factory(
    models.ProductImage, fields=('image', 'caption'), extra=1)


class MerchantProductCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """Allow the merchant to create a new product"""
    model = models.Product
    template_name = "m-create_new_product.html"
    fields = ['title', 'description', 'category', 'price', 'stock']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ProductImageFormSet(
                self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ProductImageFormSet(
                queryset=models.ProductImage.objects.none())  # pylint: disable=no-member
        return context

    def form_valid(self, form):
        form.instance.seller = self.request.user
        self.object = form.save()  # pylint: disable=attribute-defined-outside-init
        image_formset = ProductImageFormSet(
            self.request.POST, self.request.FILES, queryset=models.ProductImage.objects.none())  # pylint: disable=no-member
        if image_formset.is_valid():
            for image_form in image_formset.forms:
                image = image_form.save(commit=False)
                image.product = self.object
                image.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:m-list')


class MerchantOfferCreateView(CreateView):  # pylint: disable=too-many-ancestors
    """allow the merchant to create and apply new offers"""
    model = models.Offer
    fields = ['title', 'products', 'discount', 'promo_code']
    template_name = "m-create_new_offer.html"

    def get_success_url(self):
        return reverse_lazy('products:m-list')

# endregion
