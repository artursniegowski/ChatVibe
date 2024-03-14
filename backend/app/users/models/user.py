"""
Custom user model.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager
from utils.abstracts import Model


class User(AbstractBaseUser, Model, PermissionsMixin):
    """Custom defined user model"""

    email = models.EmailField(
        _("email address"),
        db_index=True,
        max_length=255,
        unique=True,
        blank=False,
        help_text=_("Required. It has to be a valid email, max 255 characters."),
        error_messages={
            "unique": _("This email address already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into the admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta(AbstractBaseUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def get_full_name(self) -> str | None:
        """Returns the firs and last name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name.title()} {self.last_name.title()}"
        return None

    @property
    def get_short_name(self):
        """Return the short name for the user - first name."""
        return self.first_name

    @property
    def activate_user(self):
        """Basic method to activate a user"""
        self.is_active = True
        self.save()
        return self

    def save(self, *args, **kwargs) -> None:
        """Adding the cleaning of first_name and last_name to the save method"""
        self.first_name = self.first_name.strip() if self.first_name else ""
        self.last_name = self.last_name.strip() if self.last_name else ""
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Returns the string representation of the user model."""
        return self.email
