# Generated by Django 4.2.7 on 2023-11-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_last_update',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата создания'),
        ),
    ]
