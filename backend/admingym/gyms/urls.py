"""Urls gym module."""

# Django
from django.urls import include, path

# Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from admingym.gyms.views import ClientViewSet, GymViewSet

router = DefaultRouter()
router.register(r'gyms', GymViewSet, basename='gyms')
router.register(
    r'gyms/(?P<slug_name>[a-zA-Z0-9_-]+)/clients',
    ClientViewSet,
    basename='clients'
)

urlpatterns = [
    path('', include(router.urls))
]
