"""views for browsing, and offering products"""
from django.views.generic import ListView
from .models import Product

# region - buyer end


class ProductListView(ListView):
    """view for the buyers to browse products by categories"""
    model = Product
    template_name = "TEMPLATE_NAME"


# endregion

# region - merchant end

# endregion
