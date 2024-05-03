from typing import Tuple, TypeVar

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token

AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


class JWTCookieAuthentication(JWTAuthentication):
    """Using the the tokens from the cookeis from authentications"""

    def authenticate(self, request: Request) -> Tuple[AuthUser, Token] | None:

        raw_token = self._get_cookie_access_toke(request)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def _get_cookie_access_toke(self, request: Request) -> bytes:
        """
        Extracts the cookie containing the JSON access web token from the given
        request.
        """
        access_token_name = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_COOKIE_NAME", "access_token"
        )
        cookie_access_token = request.COOKIES.get(access_token_name, None)

        if isinstance(cookie_access_token, str):
            # Work around django test client oddness
            cookie_access_token = cookie_access_token.encode()

        return cookie_access_token
