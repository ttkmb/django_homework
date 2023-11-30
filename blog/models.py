from django.db import models

nullable = {'blank': True, 'null': True}


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='Слаг', **nullable)
    content = models.TextField(verbose_name='Содержимое', **nullable)
    preview = models.ImageField(upload_to='images/', **nullable, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title} ({self.slug})'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
