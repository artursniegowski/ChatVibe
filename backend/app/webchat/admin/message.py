"""Message admin customization"""

from django.contrib import admin

from webchat.models import Message


class MessageAdmin(admin.ModelAdmin):
    """Define the admin pages for the Message model."""

    ordering = ["-created"]
    list_display = ["conversation", "sender", "created", "modified"]
    list_filter = ["conversation", "sender", "created", "modified"]
    search_fields = ["conversation__channel_id", "sender__email"]
    readonly_fields = ["id", "created", "modified"]


admin.site.register(Message, MessageAdmin)
