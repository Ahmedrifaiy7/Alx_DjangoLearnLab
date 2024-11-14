from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.view_documents, name='view_documents'),
    path('documents/create/', views.create_document, name='create_document'),
    path('documents/<int:document_id>/edit/', views.edit_document, name='edit_document'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
]
