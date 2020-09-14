"""Gym views."""

# Django REST framework
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response

# Models
from admingym.gyms.models import Gym

# Permissions
from rest_framework.permissions import IsAuthenticated
from admingym.gyms.permissions import IsOwner

# Serializers
from admingym.gyms.serializers import GymModelSerializer, CreateGymModelSerializer


class GymViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Gym view set."""

    queryset = Gym.objects.filter(is_active=True)
    lookup_field = 'slug_name'

    def get_permissions(self):
        """Assing permission base on action."""

        permission_classes = [IsAuthenticated, ]

        if self.action != 'create':
            permission_classes.append(IsOwner)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Use serializer depending on the action."""

        if self.action in ['create', 'retrieve']:
            return CreateGymModelSerializer

        return GymModelSerializer

    def destroy(self, request, *args, **kwargs):
        """Send data of the user who makes the request to update their data."""
        instance = self.get_object()
        self.perform_destroy(instance, request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance, request):
        """Override delete the object and set the is_active field to False"""
        instance.is_active = False
        instance.save()

        # Update stats user
        user = request.user
        gyms = Gym.objects.filter(owner=user).count()

        if gyms <= 1:
            user.already_owns = False
            user.save()
