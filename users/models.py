from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    avatar = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Номер телефона', unique=True)
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name='Страна')
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
