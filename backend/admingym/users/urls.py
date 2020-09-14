"""Urls users module."""

# Django
from django.urls import include, path

# Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from admingym.users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
