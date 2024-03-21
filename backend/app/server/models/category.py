"""Category class - table representation"""

import os
import uuid

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.validators import FileSizeValidator
from utils.abstracts import Model


def category_icon_file_path(instance: "Category", file_name: str) -> str:
    """
    Generates file path for new the icon file / image.
    """
    ext = os.path.splitext(file_name)[1]
    if not ext:
        raise ValueError(_("Extension is missing."))
    file_name = f"{uuid.uuid4()}{ext}"
    # file will be uploaded to MEDIA_ROOT/uploads/category/icon/<UUID>.ext
    return os.path.join("uploads", "category", "icon", file_name)


class Category(Model):
    """Category class defined"""

    name = models.CharField(
        _("name"),
        null=False,
        blank=False,
        unique=True,
        max_length=100,
        validators=[MinLengthValidator(2)],
    )
    description = models.CharField(
        _("description"), max_length=300, blank=True, null=True
    )
    icon = models.FileField(
        _("icon"),
        null=True,
        blank=True,
        upload_to=category_icon_file_path,
        # max size 250KB as we expect something like a .svg
        validators=[FileSizeValidator(max_file_size=250, size_in_mb=False)],
    )

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if not self.name:  # Check if name is empty after stripping whitespace
            raise ValueError(_("Name cannot be empty"))
        # deleting previous image if it exists before saving the new one
        try:
            exisitng = Category.objects.get(id=self.id)
        except Category.DoesNotExist:
            exisitng = None

        if exisitng and exisitng.icon and exisitng.icon != self.icon:
            exisitng.icon.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
