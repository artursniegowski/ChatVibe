from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.schema import register_post_docs
from users.serializers import RegisterSerializer

# needed for the cooki http only documentaiotn - for openapi - drf - spectacular
# https://github.com/tfranzel/drf-spectacular/issues/264
from utils.jwt_tokens.openapi import JWTCookieOpenApiAuthenticationExtension  # noqa


@extend_schema_view(post=register_post_docs)  # adding openAPI doc
class RegisterView(APIView):
    """
    Register a new user.

    This endpoint allows users to register by providing their email and password.

    Request Body:
        - email (string): Email address of the user to be registered.
        - password (string): Password for the new user account.

    Example:
        ```
        {
            "email": "user@example.com",
            "password": "password123"
        }
        ```

    Responses:
        - 201 Created: User successfully registered.
        - 400 Bad Request: Bad request, validation error(s) occurred.
        - 409 Conflict: Conflict, email already exists or is not allowed.

    URL: `/api/register/`
    """

    serializer_class = RegisterSerializer

    def post(self, request: Request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            # just for example
            forbidden_emails = ["admin@admin.com", "root@root.com"]

            if email in forbidden_emails:
                return Response(
                    {"error": "Email not allowed."}, status.HTTP_409_CONFLICT
                )

            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
