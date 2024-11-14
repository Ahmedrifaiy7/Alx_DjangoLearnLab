from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Document

# View all documents (only for users with can_view permission)
@permission_required('relationship_app.can_view', raise_exception=True)
def view_documents(request):
    documents = Document.objects.all()
    return render(request, 'relationship_app/view_documents.html', {'documents': documents})

# Create a new document (only for users with can_create permission)
@permission_required('relationship_app.can_create', raise_exception=True)
def create_document(request):
    if request.method == 'POST':
        # Logic to handle form submission
        pass
    return render(request, 'relationship_app/create_document.html')

# Edit a document (only for users with can_edit permission)
@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        # Logic to handle form submission
        pass
    return render(request, 'relationship_app/edit_document.html', {'document': document})

# Delete a document (only for users with can_delete permission)
@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('view_documents')