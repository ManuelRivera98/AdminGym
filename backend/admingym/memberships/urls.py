"""Urls membership module."""

# Django
from django.urls import include, path

# Django REST framework
from rest_framework.routers import DefaultRouter

# Views
from admingym.memberships.views import MembershipViewSet

router = DefaultRouter()
router.register(r'memberships/(?P<slug_name>[a-zA-Z0-9_-]+)/clients', MembershipViewSet, basename='memberships')

urlpatterns = [
    path('', include(router.urls))
]
