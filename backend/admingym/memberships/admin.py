"""Membership admin."""

# Django
from django.contrib import admin

# Models
from admingym.memberships.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    """Membership admin."""
    pass
