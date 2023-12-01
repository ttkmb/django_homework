from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from django.core.mail import send_mail

from blog.models import Post
from config import settings


class PostListView(ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление нового поста'
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()

        if self.object.count_views == 100:
            send_mail(subject='TEST',
                      message='test',
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=['qfFkA@example.com'],
                      fail_silently=False)
        return self.object


class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        if form.is_valid():
            form.title = form.slug = form.content = form.preview = form.created_at = form.is_published = form.count_views = self.request.user
            form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление поста'
        return context

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:posts')
