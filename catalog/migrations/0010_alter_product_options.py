# Generated by Django 4.2.7 on 2024-01-24 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_publish', 'Может опубликовать')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
