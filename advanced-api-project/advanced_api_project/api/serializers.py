from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

# BookSerializer handles serialization and validation for the Book model.
# Custom validation ensures the publication year is not in the future.

# AuthorSerializer includes a nested BookSerializer for dynamically serializing related books.
# The `books` field uses `read_only=True` to prevent updating books via the Author serializer.
