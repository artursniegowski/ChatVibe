from typing import Any, Dict, TypeVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """based on the simple jwt TokenRefreshSerializer making sure the refresh token can
    still be accessed corectly according to the tokens with cookies.
    Extending the functionality that is to retrvie the refresh token
    from the cookies insted of the request body or headers."""

    refresh = None

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token_name = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token"
        )

        attrs["refresh"] = self.context["request"].COOKIES.get(refresh_token_name, None)

        if attrs["refresh"]:
            return super().validate(attrs)

        raise InvalidToken
