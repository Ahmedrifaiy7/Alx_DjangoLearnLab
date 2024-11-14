from django.shortcuts import get_object_or_404, render, redirect
from .models import Book
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm

def add_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to the list of books after saving
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_view', raise_exception=True)  # This line enforces permission
def book_list(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'bookshelf/book_list.html', {'books': books})
