"""base urls"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from products import urls as product_urls
from transactions import urls as transaction_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(product_urls)),
    path('user/', include(transaction_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
