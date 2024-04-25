from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import Model


class Message(Model):
    """Message table representation"""

    conversation = models.ForeignKey(
        "Conversation",
        verbose_name=_("conversation"),
        on_delete=models.CASCADE,
        related_name="message",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("sender"),
        on_delete=models.CASCADE,
        related_name="message_sender",
    )
    content = models.TextField(_("content"), blank=False, null=False)
