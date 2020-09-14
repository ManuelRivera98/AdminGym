"""Owners admin."""

# Django
from django.contrib import admin

# Models
from admingym.users.models import Gym


@admin.register(Gym)
class OwnerAdmin(admin.ModelAdmin):
    """Owner admin."""

    list_display = ('owner', 'name', 'phone_number')
    search_fields = ('owner__username', 'phone_number', 'name')
    list_filter = ('created_at', 'updated_at')
    list_display_links = ('name', )

    fieldsets = (
        ('Gym', {
            'fields': (
                ('name', 'phone_number', 'owner__first_name')
            ),
        }),
        (None, {
            'fields': (
                ('created_at', 'updated_at')
            ),
        })
    )

    readonly_fields = 'created_at', 'updated_at'
