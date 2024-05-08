from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class LogOutAPIView(APIView):
    """used to clear the http only cookies - like access and refresh token"""

    def post(self, request, format=None):
        response = Response("Logged out successfully")
        refresh_token_name = refresh_token_name = getattr(
            settings, "SIMPLE_JWT", {}
        ).get("JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token")
        access_token_name = self.access_token_name = getattr(
            settings, "SIMPLE_JWT", {}
        ).get("JWT_AUTH_COOKIE_NAME", "access_token")
        # deleting the http only cookies
        response.set_cookie(refresh_token_name, "", expires=0)
        response.set_cookie(access_token_name, "", expires=0)

        return response
