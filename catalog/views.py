from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView

from catalog.forms import AddProductForm, VersionForm
from catalog.models import Product, UserData, Version


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
    form_class = AddProductForm
    extra_context = {'title': 'Добавление нового продукта'}
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = AddProductForm
    extra_context = {'title': 'Редактирование продукта'}
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1, can_delete=False)
        if self.request.method == 'POST':
            formset = Formset(self.request.POST, self.request.FILES, instance=self.object, prefix='version')
        else:
            formset = Formset(instance=self.object)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        self.object.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductsListView(ListView):
    paginate_by = 4
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for product in context['object_list']:
            active_version = product.versions.filter(current_version=True).first()
            if active_version:
                product.active_version = active_version
            else:
                product.active_version = None
        return context
