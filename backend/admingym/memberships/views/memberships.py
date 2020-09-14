"""Memberships views."""


# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404

# Models
from admingym.gyms.models import Gym
from admingym.memberships.models import Membership

# Serializers
from admingym.memberships.serializers import (
    MembershipModelSerializer,
    CreateMembershipSerializer,
)

# Permissions
from admingym.gyms.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated


class MembershipViewSet(
        mixins.RetrieveModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Membership Model view set."""

    queryset = Membership.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated, IsOwner, ]

    def dispatch(self, request, *args, **kwargs):
        """get object before running the whole view."""
        slug_name = kwargs['slug_name']
        self.gym = get_object_or_404(
            Gym,
            slug_name=slug_name
        )

        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """Return the gym client using the unique identity document."""

        obj = get_object_or_404(
            Membership,
            paid_for__cc=self.kwargs['pk'],
            paid_in=self.gym,
            is_active=True,
        )

        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_context(self):
        """Add the gym object"""

        context = super(MembershipViewSet, self).get_serializer_context()
        context['gym'] = self.gym

        return context

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'createMembership':
            return CreateMembershipSerializer

        return MembershipModelSerializer

    @action(detail=False, methods=['post'])
    def createMembership(self, request, *args, **kwargs):
        """Create membership."""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context={
                'request': request,
                'gym': self.gym
            }
        )
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()

        data = MembershipModelSerializer(membership).data

        return Response(data, status=status.HTTP_201_CREATED)
