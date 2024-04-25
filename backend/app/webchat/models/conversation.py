from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import Model


class Conversation(Model):
    """Coversation table representation"""

    channel_id = models.CharField(
        _("channel_id"),
        max_length=255,
    )

    def __str__(self) -> str:
        return self.channel_id
