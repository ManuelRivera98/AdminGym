"""Membership model."""

# Django
from django.db import models

# Models
from admingym.gyms.models import Client, Gym

# Utilities
from admingym.utils.models import BaseModel


class Membership(BaseModel):
    """Memberhip model"""

    paid_for = models.ForeignKey(Client, on_delete=models.CASCADE)

    paid_in = models.ForeignKey(Gym, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(
        default=0
    )

    num_weeks = models.PositiveIntegerField(
        'Number weeks paid',
        default=0,
    )

    payment_date = models.DateTimeField()

    due_date = models.DateTimeField(
        'expire'
    )

    is_active = models.BooleanField(default=False)
