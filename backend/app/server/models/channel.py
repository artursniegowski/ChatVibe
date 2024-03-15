"""Channel class - table representation"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import Model


class Channel(Model):
    """Channel class defined"""

    name = models.CharField(_("name"), max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        related_name="channel_owner",
    )
    topic = models.CharField(_("topic"), max_length=100)
    server = models.ForeignKey(
        "Server",
        verbose_name=_("server"),
        on_delete=models.CASCADE,
        related_name="channel_server",
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
