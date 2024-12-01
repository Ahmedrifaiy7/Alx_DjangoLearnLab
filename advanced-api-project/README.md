Advanced API Project
Overview
This project is a demonstration of building an advanced API using Django REST Framework (DRF). It features CRUD operations for managing books, leveraging DRF’s generic views, and incorporating custom serializers, permissions, and validations.

Project Features
CRUD Operations: Manage books (create, read, update, delete) through RESTful API endpoints.
Custom Serializers: Handle nested data structures and add validation for publication_year.
Permission Management: Differentiate access for authenticated and unauthenticated users.
Custom Validations: Ensure business rules, such as preventing future publication years, are enforced.
API Endpoints
Endpoint	Method	Description	Permissions
/api/books/	GET	Retrieve a list of all books	Read-only for all
/api/books/<int:pk>/	GET	Retrieve a specific book by ID	Read-only for all
/api/books/create/	POST	Create a new book	Authenticated users
/api/books/<int:pk>/update/	PUT	Update an existing book	Authenticated users
/api/books/<int:pk>/delete/	DELETE	Delete a book	Authenticated users
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone <repository-url>
cd advanced_api_project
2. Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Run Migrations
bash
Copy code
python manage.py makemigrations
python manage.py migrate
5. Start the Development Server
bash
Copy code
python manage.py runserver
Usage Instructions
1. Authentication
Use Django’s default authentication system or configure a token-based system (e.g., using rest_framework.authtoken).
For authenticated endpoints, include an Authorization header in your requests:
makefile
Copy code
Authorization: Token <your-auth-token>
2. API Testing
Use tools like Postman, curl, or HTTPie to test the endpoints.

Examples
List all books:
bash
Copy code
curl http://127.0.0.1:8000/api/books/
Create a book (authenticated):
bash
Copy code
curl -X POST -H "Authorization: Token <your-token>" -d "title=New Book&publication_year=2023&author=1" http://127.0.0.1:8000/api/books/create/
Update a book (authenticated):
bash
Copy code
curl -X PUT -H "Authorization: Token <your-token>" -d "title=Updated Book" http://127.0.0.1:8000/api/books/1/update/
Delete a book (authenticated):
bash
Copy code
curl -X DELETE -H "Authorization: Token <your-token>" http://127.0.0.1:8000/api/books/1/delete/
Custom Features
1. Validation
The BookCreateView and BookSerializer ensure publication_year cannot be in the future.
2. Permissions
Unauthenticated Users: Read-only access to the ListView and DetailView.
Authenticated Users: Full access to create, update, and delete books.
3. Relationships
The AuthorSerializer includes a nested BookSerializer to serialize books related to an author dynamically.
Project Structure
graphql
Copy code
advanced_api_project/
│
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py        # Data models for Author and Book
│   ├── serializers.py   # Custom serializers for Book and Author
│   ├── views.py         # Generic views for CRUD operations
│   ├── urls.py          # API endpoint routes
│   └── tests.py         # Test cases for the API (optional)
│
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py      # Project settings, including DRF configuration
│   ├── urls.py          # Main project URL routing
│   └── wsgi.py
│
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
Future Enhancements
Add pagination for the BookListView.
Implement search and filtering functionality.
Extend the permissions to use custom roles or groups.
Integrate token-based authentication using rest_framework.authtoken.

GET /api/books/?title=<title>        # Filter by book title
GET /api/books/?author=<author>      # Filter by author
GET /api/books/?publication_year=<year>  # Filter by publication year

GET /api/books/?search=<query>       # Search by title or author

GET /api/books/?ordering=title        # Order by title (ascending)
GET /api/books/?ordering=-publication_year  # Order by publication year (descending)

GET /api/books/?search=<query>&publication_year=<year>&ordering=-title


To implement comprehensive unit tests for your Django REST Framework (DRF) APIs, we'll cover all aspects of testing CRUD operations, filtering, searching, ordering, and permissions. This ensures that your API functions as expected in different scenarios.

Step 1: Understand What to Test
Key Areas to Test:
CRUD Operations:

Create: Test creating a Book and ensuring it's saved in the database.
Read: Test retrieving all books (ListView) and a single book (DetailView).
Update: Test updating a book and verifying the changes.
Delete: Test deleting a book and ensuring it's removed.
Filtering, Searching, and Ordering:

Test that filtering by title, author, and publication year works.
Test that searching by title and author’s name works as expected.
Test that ordering by title and publication year works.
Permissions and Authentication:

Ensure the correct permissions are enforced (e.g., authenticated users can create, update, or delete, but unauthenticated users can only view).
Step 2: Set Up Testing Environment
Configure Test Settings:
Django uses a separate test database by default, which ensures that your production or development data is not affected by tests.
You don’t need to change any settings explicitly for testing, but ensure django.test.TestCase is being used to create isolated tests.
Step 3: Write Test Cases
Create the file api/test_views.py and write tests for each of the scenarios. Here's an example implementation:
python
Copy code
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
Step 4: Run and Review Tests
To run your tests, execute the following command:

bash
Copy code
python manage.py test api
Django will automatically create a test database and run the tests. If any tests fail, it will provide details on the failed tests.
After running the tests, you should check the output in the terminal for success/failure messages.
Step 5: Document Your Testing Approach
In your README, document how to run the tests and what each test case is doing. Here's an example for the testing section:

markdown
Copy code
## Testing

### How to Run Tests
To run the tests for the API, use the following command:

```bash
python manage.py test api
Test Cases
test_create_book: Ensures a user can create a book with proper authentication.
test_create_book_unauthenticated: Tests that unauthenticated users cannot create a book.
test_list_books: Tests retrieving all books via the GET request.
test_filter_books_by_title: Tests filtering books by title.
test_search_books: Verifies searching books by title or author.
test_order_books_by_publication_year: Ensures books can be ordered by publication year.
test_update_book: Tests updating the details of a book.
test_delete_book: Verifies that a book can be deleted.

---

This setup ensures that your API is well-tested, handling CRUD operations, permissions, and advanced query functionality with appropriate responses and status codes.

