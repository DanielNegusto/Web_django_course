from django.urls import path
from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('update/<int:product_id>/', UpdateProductView.as_view(), name='update_product'),
    path('delete/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
]


