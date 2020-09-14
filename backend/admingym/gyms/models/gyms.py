"""Gym models"""

# Django
from django.db import models
from django.core.validators import RegexValidator

# Models
from admingym.users.models import User

# Utilities
from admingym.utils.models import BaseModel


class Gym(BaseModel):
    """Gym model."""

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to is digits allowed.',
    )

    slug_name_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9]$',
        message='Can not have spaces.',
    )

    # Fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=30)

    slug_name = models.CharField(
        validators=[slug_name_regex, ],
        max_length=10,
        unique=True
    )

    monthly_price = models.PositiveIntegerField(
        default=0
    )

    direction = models.CharField(
        max_length=20,
        blank=True, null=True
    )

    phone_number = models.CharField(
        # Django, before saving the value in the database, will find the validators and execute them.
        validators=[phone_regex, ],
        unique=True,
        max_length=17,
    )

    c_memberships = models.PositiveIntegerField(
        'counter memberships',
        default=0,
        help_text='Gym Membership Counter'
    )

    is_active = models.BooleanField(
        default=False,
        help_text='Manage status when deleting a gym object'
    )

    is_official = models.BooleanField(default=False)

    def __str__(self):
        """Return first name"""
        return self.name
