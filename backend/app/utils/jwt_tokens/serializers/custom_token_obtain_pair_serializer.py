from typing import Any, Dict, TypeVar

from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """based on the simple jwt TokenObtainPairSerializer adding extra information
    like the user_id"""

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        """adding custom data to the token payload"""
        # customizign get_token by adding the user_id
        token = super().get_token(user)
        # adding specific data as payload to the token
        # just an example how to do it
        token["example"] = "example"

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """adding custom data to the response"""
        data = super().validate(attrs)
        # addign additional data - user_id
        data["user_id"] = self.user.id

        return data
