"""
Django admin customization - custom user model.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for user model."""

    # add_form = UserCreationForm  # no need to define as same name as default
    # form = UserChangeForm  # no need to define as same name as default
    ordering = ["email"]
    list_display = [
        # "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "created",
        "modified",
    ]
    list_display_links = ["email"]
    list_filter = ["email", "first_name", "last_name", "is_staff", "is_active"]

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password", "id")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "modified", "created")}),
    )
    readonly_fields = ["modified", "created", "last_login", "id"]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_staff", "is_active", "is_superuser")}),
    )

    search_fields = ["email", "first_name", "last_name"]


admin.site.register(User, UserAdmin)
