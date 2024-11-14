## Group-Based Access Control in Django

This application uses Django’s groups and permissions to control access to `Document` instances.

### Groups and Permissions
- **Viewers**: Can only view documents.
- **Editors**: Can view, create, and edit documents.
- **Admins**: Full access, including viewing, creating, editing, and deleting documents.

### Setting Up Groups
Use Django Admin or the provided script in `relationship_app/scripts` to create the groups and assign permissions automatically.
