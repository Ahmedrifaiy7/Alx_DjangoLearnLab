from django.urls import path

from . import views
from .views import RegisterView, LoginView

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', views.follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow-user'),

]
