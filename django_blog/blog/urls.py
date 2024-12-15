from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import post_search

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from .views import post_detail, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/', post_detail, name='post-detail'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('search/', post_search, name='post-search'),
    path('tags/<str:tag_name>/', post_by_tag, name='tagged-posts'),
    path('tags/<str:tag_name>/', views.tagged_posts, name='tagged_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('', views.PostListView.as_view(), name='post-list'),  # List all posts
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),  # View a specific post
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),  # Create a new post
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  # Update a post
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  # Delete a post
    # Comment-related URLs
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
     path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts_by_tag'),
]
