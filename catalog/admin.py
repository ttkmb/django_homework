from django.contrib import admin

from catalog.models import Category, Product, UserData


# Register your models here.

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(UserData)
class AdminUserData(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email')
