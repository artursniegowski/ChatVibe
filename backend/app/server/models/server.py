"""Server class - table representation"""

import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.validators import ImageSizeValidator, validate_image_file_extension
from utils.abstracts import Model


def server_icon_file_path(instance: "Server", file_name: str) -> str:
    """
    Generates file path for new the icon file / image.
    """
    ext = os.path.splitext(file_name)[1]
    if not ext:
        raise ValueError(_("Extension is missing."))
    file_name = f"{uuid.uuid4()}{ext}"
    # file will be uploaded to MEDIA_ROOT/uploads/server/icon/<UUID>.ext
    return os.path.join("uploads", "server", "icon", file_name)


def server_banner_file_path(instance: "Server", file_name: str) -> str:
    """
    Generates file path for new the banner file / image.
    """
    ext = os.path.splitext(file_name)[1]
    if not ext:
        raise ValueError(_("Extension is missing."))
    file_name = f"{uuid.uuid4()}{ext}"
    # file will be uploaded to MEDIA_ROOT/uploads/server/banner/<UUID>.ext
    return os.path.join("uploads", "server", "banner", file_name)


class Server(Model):
    """Server class defined"""

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
    banner = models.ImageField(
        _("banner"),
        null=True,
        blank=True,
        upload_to=server_banner_file_path,
        validators=[
            ImageSizeValidator(max_width=3000, max_height=3000),
            validate_image_file_extension,
        ],
    )
    icon = models.ImageField(
        _("icon"),
        null=True,
        blank=True,
        upload_to=server_icon_file_path,
        validators=[ImageSizeValidator(70, 70), validate_image_file_extension],
    )

    def save(self, *args, **kwargs) -> None:
        # deleting previous image (icon, banner) if it exists before saving the new one
        try:
            exisitng = Server.objects.get(id=self.id)
        except Server.DoesNotExist:
            exisitng = None

        if exisitng:
            if exisitng.icon and exisitng.icon != self.icon:
                exisitng.icon.delete(save=False)
            if exisitng.banner and exisitng.banner != self.banner:
                exisitng.banner.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
