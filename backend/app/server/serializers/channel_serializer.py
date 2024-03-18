from rest_framework import serializers

from server.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    """Serializes data for channel"""

    class Meta:
        model = Channel
        fields = "__all__"
