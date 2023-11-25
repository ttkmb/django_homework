from django.urls import path

from catalog.apps import MainConfig
from catalog.views import index, contact, product, add_product, list_products

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contact, name='contact'),
    path('product/<int:product_id>/', product, name='product'),
    path('add_product/', add_product, name='add_product'),
    path('products/', list_products, name='list_product'),
]