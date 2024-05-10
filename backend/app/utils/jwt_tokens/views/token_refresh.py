"""
Redefining the refresh token view from rest_framework_simplejwt, so it can
handle the authentication with the HTTP only cookie
"""

from drf_spectacular.utils import extend_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from utils.jwt_tokens.mixins.jwt_set_cookie_mixin import JWTSetCookieMixin
from utils.jwt_tokens.schema import token_refresh_post_schema


@extend_schema_view(post=token_refresh_post_schema)  # adding openAPI doc
class JWTCookieTokenRefreshView(JWTSetCookieMixin, TokenRefreshView):
    """
    TokenRefreshView with JWT HTTP-only cookie

    A New Access token will be set as HTTP-only cookie if the refresh token is valid
    and exists in the http-only cookie.
    """

    pass
