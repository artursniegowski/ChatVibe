"""
Redefining the obtain pair token view from rest_framework_simplejwt, so it can
handle the authentication with the HTTP only cookie
"""

from rest_framework_simplejwt.views import TokenObtainPairView

from utils.jwt_tokens.jwt_set_cookie_mixin import JWTSetCookieMixin


class JWTCookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    """TokenObtainPairView with jwt http only cookie"""

    pass
