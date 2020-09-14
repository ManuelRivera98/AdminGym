"""Permissions gym"""

# Django REST framework
from rest_framework.permissions import BasePermission

# Models
from admingym.gyms.models import Gym


class IsOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        """Retrieve the object overridden by the lookup_field field of the class"""
        obj = Gym
        return self.has_objects_permission(request, view, obj)

    def has_objects_permission(self, request, view, obj):
        """Check that the user of the request owns the gym"""

        try:
            access = obj.objects.get(
                slug_name=view.kwargs['slug_name'],
                owner=request.user,
                is_active=True,
            )
        except obj.DoesNotExist:
            return False

        if access:
            return True

        return False
