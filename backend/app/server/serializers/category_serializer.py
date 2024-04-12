from rest_framework import serializers

from server.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializes data for category"""

    class Meta:
        model = Category
        fields = "__all__"
