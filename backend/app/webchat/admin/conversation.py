"""Conversation admin customization"""

from django.contrib import admin

from webchat.models import Conversation


class ConversationAdmin(admin.ModelAdmin):
    """Define the admin pages for the Conversation model."""

    ordering = ["-created"]
    list_display = ["channel_id", "created", "modified"]
    list_filter = ["channel_id", "created", "modified"]
    search_fields = ["channel_id"]
    readonly_fields = ["id", "created", "modified"]


admin.site.register(Conversation, ConversationAdmin)
