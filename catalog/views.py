from django.shortcuts import render
from catalog.models import Product, UserData


def index(request):
    products = Product.objects.order_by('-id')[:5]
    for product in products:
        print(f'Наименование: {product.name}\n'
              f'Категория: {product.category}\n'
              f'Цена: {product.price}\n'
              f'----------------------------')
    return render(request, 'catalog/index.html')


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
