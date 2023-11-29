from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from catalog.models import Product, UserData


class IndexView(TemplateView):
    model = Product
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().order_by('-price')[:3]
        context['title'] = 'Самые дорогие товары'
        return context


class ContactCreateView(CreateView):
    model = UserData
    fields = ['name', 'surname', 'email']
    success_url = reverse_lazy('catalog:contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = UserData.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:index')


class ProductsListView(ListView):
    paginate_by = 1
    model = Product
