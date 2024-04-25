from rest_framework import serializers

from webchat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Message serializer"""

    # sender = serializers.StringRelatedField()
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_sender(self, obj: Message) -> str:
        """Custom method to return the sender's full name"""
        return obj.sender.get_full_name
