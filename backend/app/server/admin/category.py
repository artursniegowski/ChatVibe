"""Category admin customization"""

from django.contrib import admin

from server.models import Category


class CategoryAdmin(admin.ModelAdmin):
    """Define the admin pages for Category model."""

    ordering = ["name"]
    list_display = ["name", "created", "modified"]
    list_filter = ["name", "created", "modified"]
    search_fields = ["name"]
    readonly_fields = ["id", "created", "modified"]


admin.site.register(Category, CategoryAdmin)
