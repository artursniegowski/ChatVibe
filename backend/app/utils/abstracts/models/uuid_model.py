"""
Base model to replace the id with a UUID
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDModel(models.Model):
    """base model to replace the id with UUID"""

    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
