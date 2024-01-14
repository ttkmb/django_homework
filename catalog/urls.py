from django.urls import path

from catalog.apps import MainConfig
from catalog.views import IndexView, ContactCreateView, ProductDetailView, ProductCreateView, ProductsListView, \
    ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactCreateView.as_view(), name='contact'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('products/', ProductsListView.as_view(), name='list_product'),
]