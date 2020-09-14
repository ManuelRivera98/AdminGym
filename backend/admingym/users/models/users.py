"""Owner model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Validators => Allows us to validate a field against a regular expression.
from django.core.validators import RegexValidator

# Utilities
from admingym.utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """Owner gym model."""

    # Regex validations
    cc_regex = RegexValidator(
        regex=r'\d{8,10}$',
        message='Identification number must be of type 1,000,000',
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
        unique=True
    )

    is_verified = models.BooleanField(
        'verified client',
        default=False,
        help_text='set to true when the user have verified its email address.'
    )

    already_owns = models.BooleanField(
        'active user gym',
        default=False,
        help_text='The user must have a gym as a property in order to use the app, this field will be active when creating a gym object.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'cc', 'first_name', 'last_name']

    def __str__(self):
        """Return name's gym"""
        return self.username

    def __get_short_name(self):
        """Return name as identifier on the db."""
        return self.username
