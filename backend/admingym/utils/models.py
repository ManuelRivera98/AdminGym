"""Django models utils"""

# Django
from django.db import models


class BaseModel(models.Model):
    """
        Base Model.

        BaseModel acts as an abstract base class from which every
        other model in the project will inherit. This class provides every table with the following attributes:
            + created_at (Datetime): Store the datetime the object was created.
            + updated_at (Datetime): Store the last datetime the object was modified.
    """

    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )

    updated_at = models.DateTimeField(
        'Updated at',
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta options."""

        abstract = True

        get_latest_by = 'created_at'
        ordering = ['created_at', '-updated_at']
