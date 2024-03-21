"""Channel class - table representation"""

import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.validators import ImageSizeValidator, validate_image_file_extension
from utils.abstracts import Model


def channel_icon_file_path(instance: "Channel", file_name: str) -> str:
    """
    Generates file path for new the icon file / image.
    """
    ext = os.path.splitext(file_name)[1]
    if not ext:
        raise ValueError(_("Extension is missing."))
    file_name = f"{uuid.uuid4()}{ext}"
    # file will be uploaded to MEDIA_ROOT/uploads/channel/icon/<UUID>.ext
    return os.path.join("uploads", "channel", "icon", file_name)


def channel_banner_file_path(instance: "Channel", file_name: str) -> str:
    """
    Generates file path for new the banner file / image.
    """
    ext = os.path.splitext(file_name)[1]
    if not ext:
        raise ValueError(_("Extension is missing."))
    file_name = f"{uuid.uuid4()}{ext}"
    # file will be uploaded to MEDIA_ROOT/uploads/channel/banner/<UUID>.ext
    return os.path.join("uploads", "channel", "banner", file_name)


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
    banner = models.ImageField(
        _("banner"),
        null=True,
        blank=True,
        upload_to=channel_banner_file_path,
        validators=[
            ImageSizeValidator(max_width=3000, max_height=3000),
            validate_image_file_extension,
        ],
    )
    icon = models.ImageField(
        _("icon"),
        null=True,
        blank=True,
        upload_to=channel_icon_file_path,
        validators=[ImageSizeValidator(70, 70), validate_image_file_extension],
    )

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.strip().lower()
        # deleting previous image (icon, banner) if it exists before saving the new one
        try:
            exisitng = Channel.objects.get(id=self.id)
        except Channel.DoesNotExist:
            exisitng = None

        if exisitng:
            if exisitng.icon and exisitng.icon != self.icon:
                exisitng.icon.delete(save=False)
            if exisitng.banner and exisitng.banner != self.banner:
                exisitng.banner.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
