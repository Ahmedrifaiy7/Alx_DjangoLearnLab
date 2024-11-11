from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView, add_book, edit_book, delete_book, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books

urlpatterns = [
    path('books/', views.list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
    path('books/add/', add_book, name='add_book'),
    path('books/edit/<int:book_id>/', edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', delete_book, name='delete_book'),
    path('books/', list_books, name='list_books'),  # Add the URL pattern
    path('register/', views.register, name='register'),  # URL for registration view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # URL for login view
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # URL for logout view
    path('books/', views.list_books, name='list_books'),  # Existing URL for listing books
    path('add_book/', views.add_book, name='add_book'),  # URL for adding a book
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),  # URL for editing a book
    path('books/', views.list_books, name='list_books'),  # Existing URL for listing books
]

