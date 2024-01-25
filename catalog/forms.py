from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Product, Version, Category


class AddProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Выберите категорию')

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Название продукта'}),
            'description': forms.Textarea(
                attrs={'cols': 50, 'rows': 5, 'class': 'form-input', 'placeholder': 'Описание продукта'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'class': 'form-input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        for word in banned_words:
            if word in name.lower():
                self.add_error('name', f'Слово {word} запрещено')
            if word in description.lower():
                self.add_error('description', f'Слово {word} запрещено')


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['version_number', 'version_name', 'current_version']
        widgets = {
            'version_number': forms.NumberInput(attrs={'class': 'form-input'}),
            'version_name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean(self):
        product = Product.objects.get(id=self.cleaned_data['product'].id)
        active_version = self.cleaned_data['current_version']
        count_versions = product.versions.filter(current_version=True).count()
        if active_version and (count_versions + 1) > 1:
            raise forms.ValidationError(
                "У продукта может быть только одна активная версия, пожалуйста, выберите только одну активную версию")


class ModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'category', 'is_published']
        widgets = {
            'description': forms.Textarea(
                attrs={'cols': 50, 'rows': 5, 'class': 'form-input', 'placeholder': 'Описание продукта'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-input'})
        }