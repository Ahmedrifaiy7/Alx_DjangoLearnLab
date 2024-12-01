from django.contrib import admin
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
    from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Document


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Define groups and their permissions
groups_permissions = {
    "Viewers": ["can_view"],
    "Editors": ["can_view", "can_edit", "can_create"],
    "Admins": ["can_view", "can_edit", "can_create", "can_delete"],
}

# Create groups and assign permissions
for group_name, permissions in groups_permissions.items():
    group, created = Group.objects.get_or_create(name=group_name)
    for perm_name in permissions:
        content_type = ContentType.objects.get_for_model(Document)
        permission = Permission.objects.get(
            codename=perm_name,
            content_type=content_type,
        )
        group.permissions.add(permission)
admin.site.register(Book)
