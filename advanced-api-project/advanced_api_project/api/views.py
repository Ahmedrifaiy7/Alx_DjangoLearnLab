from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from django.shortcuts import render
from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filterset_fields = ['title', 'author', 'publication_year']  # Fields to filter by
    search_fields = ['title', 'author__name']  # Search by title and author's name
    ordering_fields = ['title', 'publication_year']  # Fields to order by
    ordering = ['title']  # Default ordering (ascending title)


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create books

    def perform_create(self, serializer):
        publication_year = self.request.data.get('publication_year')
        if int(publication_year) > datetime.now().year:
            raise ValidationError({"publication_year": "Publication year cannot be in the future."})
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can update books

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can delete books

# BookListView: Handles listing all books, open to unauthenticated users.
# BookDetailView: Retrieves a single book by ID, accessible to all users.
# BookCreateView: Allows authenticated users to create a new book.
# BookUpdateView: Allows authenticated users to update a book's details.
# BookDeleteView: Allows authenticated users to delete a book.
