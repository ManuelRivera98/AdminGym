"""Clients models."""

# Django
from django.db import models
from django.core.validators import RegexValidator

# Models
from admingym.gyms.models import Gym

# Utilities
from admingym.utils.models import BaseModel


class Client(BaseModel):
    """Client models"""

    # Regex validations

    cc_regex = RegexValidator(
        regex=r'\d{8,10}$',
        message='Identification number must be of type 1,000,000,000',
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to is digits allowed.',
    )

    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=10)

    last_name = models.CharField(max_length=10)

    phone_number = models.CharField(
        validators=[phone_regex, ],
        unique=True,
        max_length=17,
        blank=True, null=True,
    )

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exits.'
        }
    )

    cc = models.CharField(
        validators=[cc_regex, ],
        max_length=10,
        unique=True,
        help_text='Unique National Identity Document'
    )

    c_memberships = models.PositiveIntegerField(
        default=0,
        help_text='Number of times the membership has been paid'
    )

    is_active = models.BooleanField(
        default=False,
        help_text='Handle in case of membership expiration'
    )

    def __str__(self):
        return '{} cc: {} '.format(self.first_name, self.cc)
