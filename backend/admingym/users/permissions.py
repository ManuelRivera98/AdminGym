"""User permissions."""

# Django REST framework
from rest_framework.permissions import BasePermission

# Model
from admingym.users.models import User


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        """Retrieve the object overridden by the lookup_field field of the class"""
        obj = User.objects.get(username=view.kwargs['username'])
        return self.has_objects_permission(request, view, obj)

    def has_objects_permission(self, request, view, obj):
        """Check object and user are the same."""

        return request.user == obj
