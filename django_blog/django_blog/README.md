Django Blog Project: Authentication System
This project includes a comprehensive user authentication system with features such as registration, login, logout, and profile management. This document explains how to set up and test the authentication system and provides guidance for extending the functionality.

Features
User Registration: Create new user accounts with a username, email, and password.
User Login/Logout: Secure user authentication and session management.
Profile Management: View and edit user profiles, including email and additional profile fields.
Setup Instructions
Prerequisites
Python 3.x installed on your system
Django installed (pip install django)
A working Django project named django_blog
Step 1: Install Dependencies
Install the required Python packages:

bash
Copy code
pip install django
Step 2: Create the Blog App
If not already done, create the blog app:

bash
Copy code
python manage.py startapp blog
Register the app in INSTALLED_APPS in django_blog/settings.py:

python
Copy code
INSTALLED_APPS = [
    ...
    'blog',
]
Step 3: Configure URL Patterns
Update django_blog/urls.py to include the blog app's URLs:

python
Copy code
from django.urls import path, include

urlpatterns = [
    path('', include('blog.urls')),
]
In blog/urls.py, define paths for login, logout, registration, and profile management:

python
Copy code
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
Step 4: Create and Migrate Database
Run the following commands to apply migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Step 5: Create Templates
Add the following templates in blog/templates/blog/:

login.html: For user login
register.html: For user registration
profile.html: For viewing and editing profiles
Ensure each template includes {% csrf_token %} for security.

Step 6: Test the Authentication System
Run the Server: Start the development server:

bash
Copy code
python manage.py runserver
Access the Pages:

Registration: Navigate to /register to create a new user account.
Login: Go to /login to authenticate with your credentials.
Profile: After login, visit /profile to view your profile.
Logout: Use /logout to log out.
Verify the Features:

Test form validation, including required fields and password rules.
Confirm error handling for invalid login attempts or registration errors.
Extending the User Model
Adding Custom Fields
To add fields like a bio or profile picture, extend the User model using a one-to-one relationship:

python
Copy code
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
Run migrations after creating the model:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Updating the Profile View
Update the profile view to include additional fields:

python
Copy code
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileUpdateForm(instance=request.user.userprofile)
    return render(request, 'blog/profile.html', {'form': form})
Testing the Features
Use Django’s development server (python manage.py runserver) to test the system in a browser.
Ensure all forms include {% csrf_token %} for security.
Verify that:
Registration prevents duplicate usernames or emails.
Login works only with valid credentials.
Profile updates reflect immediately in the database.
Next Steps
Add password reset functionality.
Allow users to upload a profile picture.
Implement email confirmation for new registrations.
Features
View all posts.
Create new posts.
Edit or delete existing posts (author-only).
Permissions to ensure security.
Setup Instructions
Add Post model to models.py (already done).
Configure URLs in blog/urls.py (as above).
Add templates for all CRUD views.
Run migrations:
bash
Copy code
Comment System
Add a Comment: Logged-in users can post a comment on any blog post. The comment will be associated with the post and the user.
Edit/Delete Comments: Users can edit or delete their own comments.
Permissions: Only the author of a comment can edit or delete it. Other users cannot modify comments.