"""User models admin"""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from admingym.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'cc', 'is_verified', 'already_owns', 'is_active')
    list_filter = ('is_verified', 'username')
    list_display_links = ('username', 'email')

    fieldsets = (
        ('Gym', {
            'fields': (
                ('first_name', 'last_name', 'username', 'email'), ('cc', 'already_owns')
            ),
        }),
        ('Password', {
            'fields': (
                'password',
            )
        }),
        ('Metadata', {
            'fields': (
                ('is_verified', 'is_active')
            ),
        }),
        (None, {
            'fields': (
                ('created_at', 'updated_at')
            ),
        })
    )

    readonly_fields = 'created_at', 'updated_at'
