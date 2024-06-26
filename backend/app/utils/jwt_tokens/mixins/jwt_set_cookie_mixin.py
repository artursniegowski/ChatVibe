"""
Mixing used for adding the http only cookie tokes to the Views.
"""

from datetime import timedelta

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response


class JWTSetCookieMixin:
    """Mixin to add JWT tokens over http only cookies"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.same_site_setting = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_SAMESITE", "Lax"
        )
        self.access_token_name = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_COOKIE_NAME", "access_token"
        )
        self.refresh_token_name = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token"
        )
        self.max_age_access_toke = getattr(settings, "SIMPLE_JWT", {}).get(
            "ACCESS_TOKEN_LIFETIME", timedelta(minutes=5).total_seconds()
        )
        self.max_age_refresh_toke = getattr(settings, "SIMPLE_JWT", {}).get(
            "REFRESH_TOKEN_LIFETIME", timedelta(days=1).total_seconds()
        )

    def _set_access_token_cookie(self, response: Response, access_token: str) -> None:
        """sets the access token as a cookie in the response"""
        response.set_cookie(
            self.access_token_name,
            access_token,
            samesite=self.same_site_setting,
            max_age=self.max_age_access_toke,
            httponly=True,
        )

    def _set_refresh_token_cookie(self, response: Response, refresh_token: str) -> None:
        """sets the refresh token as a cookie in the response"""
        response.set_cookie(
            self.refresh_token_name,
            refresh_token,
            samesite=self.same_site_setting,
            max_age=self.max_age_refresh_toke,
            httponly=True,
        )

    def finalize_response(
        self, request: Request, response: Response, *args, **kwargs
    ) -> Response:
        """
        overridden to intercept the response generated by the view.
        If the response contains access and refresh tokens, it calls
        the appropriate methods to set them as cookies.
        """
        response = super().finalize_response(request, response, *args, **kwargs)

        if hasattr(response, "data"):
            if "access" in response.data:
                access_token = response.data["access"]
                self._set_access_token_cookie(response, access_token)

                del response.data["access"]

            if "refresh" in response.data:
                refresh_token = response.data["refresh"]
                self._set_refresh_token_cookie(response, refresh_token)

                del response.data["refresh"]

        # user = response.data["user_id"]

        return response
