"""Server class - table representation"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import Model


class Server(Model):
    """Category class defined"""

    name = models.CharField(_("name"), max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        related_name="server_owner",
    )
    category = models.ForeignKey(
        "Category",
        verbose_name=_("category"),
        on_delete=models.PROTECT,
        related_name="server_category",
    )
    description = models.CharField(
        _("description"), max_length=300, blank=True, null=True
    )
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("member"),
        related_name="servers_joined",
    )

    def __str__(self) -> str:
        return self.name
