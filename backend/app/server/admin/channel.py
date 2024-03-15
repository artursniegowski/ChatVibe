"""Channel admin customization"""

from django.contrib import admin

from server.models import Channel


class ChannelAdmin(admin.ModelAdmin):
    """Define the admin pages for Channel model."""

    ordering = ["name"]
    list_display = ["name", "owner", "server", "created", "modified"]
    list_filter = ["name", "owner", "created", "server", "modified"]
    search_fields = ["name", "owner__email", "server__name"]
    readonly_fields = ["id", "created", "modified"]


admin.site.register(Channel, ChannelAdmin)
