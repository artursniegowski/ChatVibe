"""Server admin customization"""

from django.contrib import admin

from server.models import Server


class ServerAdmin(admin.ModelAdmin):
    """Define the admin pages for Server model."""

    ordering = ["name"]
    list_display = ["name", "owner", "category", "created", "modified"]
    list_filter = ["name", "owner", "category", "created", "modified"]
    search_fields = ["name", "owner__email", "category__name"]
    readonly_fields = ["id", "created", "modified"]


admin.site.register(Server, ServerAdmin)
