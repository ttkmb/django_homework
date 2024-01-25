from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView

from catalog.forms import AddProductForm, VersionForm, ModeratorForm
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = AddProductForm
    extra_context = {'title': 'Добавление нового продукта'}
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    extra_context = {'title': 'Редактирование продукта'}
    permission_required = 'catalog.change_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Formset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context['formset'] = Formset(self.request.POST, instance=self.object)
        else:
            context['formset'] = Formset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        if self.request.user.is_superuser:
            return AddProductForm
        elif self.request.user.is_staff:
            return ModeratorForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionError('Недостаточно прав для редактирования этого продукта')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')


class ProductsListView(LoginRequiredMixin, ListView):
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
