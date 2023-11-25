from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from catalog.forms import AddProductForm
from catalog.models import Product, UserData


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'title': 'Главная страница',
    }
    return render(request, 'catalog/index.html', context)


def contact(request):
    user_data = UserData.objects.all()
    context = {
        'user_data': user_data
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}, phone: {phone}, message: {message}')
    return render(request, 'catalog/contact.html', context)


def product(request, product_id):
    merchandise = get_object_or_404(Product, id=product_id)
    context = {
        'product': merchandise,
        'title': f'Страница товара {merchandise.name}'
    }
    return render(request, 'catalog/product.html', context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})


def list_products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/list_product.html', {'products': products, 'page_obj': page_obj})
