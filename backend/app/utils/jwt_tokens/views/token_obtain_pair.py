"""
Redefining the obtain pair token view from rest_framework_simplejwt, so it can
handle the authentication with the HTTP only cookie
"""

from drf_spectacular.utils import extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.jwt_tokens.mixins.jwt_set_cookie_mixin import JWTSetCookieMixin
from utils.jwt_tokens.schema import token_obtain_post_schema


@extend_schema_view(post=token_obtain_post_schema)  # adding openAPI doc
class JWTCookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    """
    TokenObtainPairView with jwt http only cookie
  
    A new access token and refresh token will be set as HTTP-only cookies if the 
    provided email and password are correct.
    """

    pass
