"""Gym models admin"""

# Django
from django.contrib import admin

# Models
from admingym.gyms.models import Gym, Client


@admin.register(Gym)
class GymModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    pass
