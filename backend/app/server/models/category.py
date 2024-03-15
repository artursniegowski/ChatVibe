"""Category class - table representation"""

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.abstracts import Model


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

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        if not self.name:  # Check if name is empty after stripping whitespace
            raise ValueError(_("Name cannot be empty"))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
