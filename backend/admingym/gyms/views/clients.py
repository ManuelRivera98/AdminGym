"""View Clients."""


# Django REST framework
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

# Django
from django.shortcuts import get_object_or_404

# Models
from admingym.gyms.models import Client, Gym
from admingym.memberships.models import Membership

# Serializers
from admingym.gyms.serializers import ClientModelSerializer, CreateModelSerializer
from admingym.memberships.serializers import MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from admingym.gyms.permissions import IsOwner


class ClientViewSet(viewsets.ModelViewSet):
    """Client view set."""

    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'cc'

    def dispatch(self, request, *args, **kwargs):
        """get object before running the whole view."""
        slug_name = kwargs['slug_name']
        self.gym = get_object_or_404(
            Gym,
            slug_name=slug_name
        )

        return super(ClientViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        """serializer base on action view."""

        if self.action == 'create':
            return CreateModelSerializer

        return ClientModelSerializer

    def get_serializer_context(self):
        """Add the gym object"""

        context = super(ClientViewSet, self).get_serializer_context()
        context['gym'] = self.gym

        return context

    def retrieve(self, request, *args, **kwargs):
        """Add membership's user."""
        response = super(ClientViewSet, self).retrieve(request, *args, **kwargs)

        client = self.get_object()
        try:
            memberships = Membership.objects.filter(paid_for=client, paid_in=self.gym)
        except Membership.DoesNotExist:
            data = {
                'detail': 'Not found',
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        else:
            data = {
                'client': response.data,
                'membership': MembershipModelSerializer(memberships, many=True).data
            }
            response.data = data

            return response
