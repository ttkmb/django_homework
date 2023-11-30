from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('', PostListView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),
]