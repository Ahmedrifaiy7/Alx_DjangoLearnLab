from django.shortcuts import get_object_or_404, render
from .models import Book
from django.contrib.auth.decorators import permission_required

def get_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Securely fetches book without direct SQL query
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@permission_required('bookshelf.can_view', raise_exception=True)  # This line enforces permission
def book_list(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})
