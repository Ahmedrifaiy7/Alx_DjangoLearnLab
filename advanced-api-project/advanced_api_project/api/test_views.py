from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author
from rest_framework.reverse import reverse


class BookAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an author for testing
        cls.author = Author.objects.create(name="Author 1")

        # Create a user for authentication
        cls.user = User.objects.create_user(username='testuser', password='password')

        # Create books for testing
        cls.book_1 = Book.objects.create(title="Book 1", publication_year=2023, author=cls.author)
        cls.book_2 = Book.objects.create(title="Book 2", publication_year=2024, author=cls.author)

    def test_create_book(self):
        # Test creating a book with authenticated user
        self.client.login(username='testuser', password='password')
        url = reverse('book-list')
        data = {'title': 'New Book', 'publication_year': 2025, 'author': self.author.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        # Test creating a book without authentication
        url = reverse('book-list')
        data = {'title': 'New Book', 'publication_year': 2025, 'author': self.author.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_books(self):
        # Test retrieving all books
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_title(self):
        # Test filtering books by title
        url = reverse('book-list') + '?title=Book 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_search_books(self):
        # Test searching for books
        url = reverse('book-list') + '?search=Book'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_publication_year(self):
        # Test ordering books by publication year
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_update_book(self):
        # Test updating a book's title
        self.client.login(username='testuser', password='password')
        url = reverse('book-detail', args=[self.book_1.id])
        data = {'title': 'Updated Book 1', 'publication_year': 2023, 'author': self.author.id}

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.title, 'Updated Book 1')

    def test_delete_book(self):
        # Test deleting a book
        self.client.login(username='testuser', password='password')
        url = reverse('book-detail', args=[self.book_1.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_permissions_on_create(self):
        # Test that unauthenticated users cannot create a book
        url = reverse('book-list')
        data = {'title': 'Unauthorized Book', 'publication_year': 2025, 'author': self.author.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_on_update(self):
        # Test that unauthenticated users cannot update a book
        url = reverse('book-detail', args=[self.book_1.id])
        data = {'title': 'Unauthorized Update', 'publication_year': 2023, 'author': self.author.id}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_on_delete(self):
        # Test that unauthenticated users cannot delete a book
        url = reverse('book-detail', args=[self.book_1.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
