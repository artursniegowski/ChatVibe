"""
Redefining the refresh token view from rest_framework_simplejwt, so it can
handle the authentication with the HTTP only cookie
"""

from rest_framework_simplejwt.views import TokenRefreshView

from utils.jwt_tokens.mixins.jwt_set_cookie_mixin import JWTSetCookieMixin


class JWTCookieTokenRefreshView(JWTSetCookieMixin, TokenRefreshView):
    """TokenRefreshView with jwt http only cookie"""

    pass
