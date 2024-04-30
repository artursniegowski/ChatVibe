from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializes data for model user"""

    class Meta:
        model = User
        fields = [
            "email",
        ]
