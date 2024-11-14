from django.shortcuts import get_object_or_404, render
from .models import Book

def get_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Securely fetches book without direct SQL query
    return render(request, 'bookshelf/book_detail.html', {'book': book})
