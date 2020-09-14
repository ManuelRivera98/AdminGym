"""User views."""

# Django REST framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from admingym.users.models import User
from admingym.gyms.models import Gym

# Serializers
from admingym.users.serializers import UserModelSerializer, UserCreateSerializer, AccountVerificationSerializer, UserLoginSerializer
from admingym.gyms.serializers import GymModelSerializer

# Permissions
from admingym.users.permissions import IsAccountOwner
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """User view set.APIView

        Handle sing up, login and account verify.
    """

    queryset = User.objects.filter(is_verified=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assing permission based on actions."""

        if self.action in ['login', 'createAccount', 'verify']:
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAccountOwner]
        else:
            permission_classes = [IsAuthenticated, ]

        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """Add extra the response, gym's user"""

        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        gyms = Gym.objects.filter(
            owner=request.user,
            is_active=True,
        )

        data = {
            'user': response.data,
            'gyms': GymModelSerializer(gyms, many=True).data
        }

        response.data = data

        return response

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, user = serializer.save()

        data = {
            'status': 'ok',
            'user': UserModelSerializer(user).data,
            'token': token,
        }

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def createAccount(self, request):
        """User create account."""
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify user"""

        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'message': 'Congratulations, you can now start using Admin Gym'
        }

        return Response(data, status=status.HTTP_200_OK)
