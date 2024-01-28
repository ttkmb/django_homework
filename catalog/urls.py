from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import MainConfig
from catalog.views import IndexView, ContactCreateView, ProductDetailView, ProductCreateView, ProductsListView, \
    ProductUpdateView, ProductDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactCreateView.as_view(), name='contact'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('add_product/', never_cache(ProductCreateView.as_view()), name='add_product'),
    path('product/<int:pk>/update/', never_cache(ProductUpdateView.as_view()), name='update_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('products/', ProductsListView.as_view(), name='list_product'),
]