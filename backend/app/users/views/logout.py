from django.conf import settings
from drf_spectacular.utils import extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.schema import logout_post_docs


@extend_schema_view(post=logout_post_docs)  # adding openAPI doc
class LogOutAPIView(APIView):
    """
    Clear HTTP-only cookies to log the user out.

    This endpoint clears the HTTP-only cookies, typically access and refresh tokens, to log the user out.

    Request Method: POST
    URL: `/logout/`

    Responses:
      - 200 OK: Logged out successfully.
    """

    def post(self, request: Request, format=None):
        """
        Clear HTTP-only cookies.

        This method clears the HTTP-only cookies, typically access and refresh tokens,
        to log the user out.

        Returns:
            Response: A response indicating successful logout.
        """
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
