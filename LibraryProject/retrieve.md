# Retrieve the Book instance
# Command
book = Book.objects.get(id=1)
book.title, book.author, book.publication_year

# Output
('1984', 'George Orwell', 1949)
