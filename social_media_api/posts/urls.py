# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other post URLs
    path('<int:pk>/like/', views.like_post, name='like-post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike-post'),
]

# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications'),
    path('mark_as_read/', views.MarkNotificationsAsReadView.as_view(), name="mark_as_read"),
]