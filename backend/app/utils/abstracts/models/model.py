"""
Base model, for every model used
"""

from .timestamped_model import TimestampedModel
from .uuid_model import UUIDModel


class Model(UUIDModel, TimestampedModel):
    """
    Base Model for every model
    """

    class Meta:
        abstract = True
