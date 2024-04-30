import uuid

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from users.schema import user_list_docs
from users.serializers import UserSerializer

User = get_user_model()


@extend_schema_view(  # adding the custom filtering atributes to our openAPI doc
    list=user_list_docs
)
class UserViewSet(viewsets.ViewSet):
    """
    View set for managing User data.
    Returns user name based on the token provided.
    Only for authenticated users.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def get_view_name(self):
        """
        Returns the user view name.
        """
        return "User data based on the token"

    def list(self, request: Request) -> Response:
        """
        Return user data based on the provided user ID.

        Parameters:
            request (Request): The HTTP request object containing query parameters.

        Returns:
            Response: A JSON response containing the serialized user data.

        Raises:
            ValidationError: If the 'by_userId' parameter is missing or not in the correct format,
            or if the user with the specified ID does not exist.

        Example:
            To retrieve user with the ID = '123e4567-e89b-12d3-a456-426614174000':

            GET /api/user?by_userId=123e4567-e89b-12d3-a456-426614174000
        """
        by_userId = request.query_params.get("by_userId")

        if not by_userId:
            raise ValidationError(detail="by_userId parameter is required.")

        try:
            uuid.UUID(str(by_userId))
            queryset_filtered = User.objects.get(id=by_userId)
        except ValueError:
            raise ValidationError(
                detail=f"User ID: '{by_userId}' is not in the right  UUID format."
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(queryset_filtered)

        return Response(serializer.data)
