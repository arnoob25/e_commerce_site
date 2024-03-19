"""views for browsing, and offering products"""
from django.views.generic import ListView, DetailView
from .models import Product

# region - buyer end


class ProductListView(ListView):
    """view for the buyers to browse products by categories"""
    model = Product
    template_name = "discover_products.html"


class ProductDetailView(DetailView):
    """view for the buyers to view a product's specifications and make an order"""
    model = Product
    template_name = "product_details.html"


# endregion

# region - merchant end

# endregion
