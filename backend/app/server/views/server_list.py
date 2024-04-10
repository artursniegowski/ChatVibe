import uuid

from django.db.models import Count
from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from server.models import Server
from server.schema import server_list_docs
from server.serializers import ServerSerializer


def is_pos_int(num: str) -> bool:
    """
    Returns True if the input is a positive integer or zero, else False.

    Args:
        num (str): The number to be checked.

    Returns:
        bool: True if the number is a positive integer or zero, else False.
    """
    try:
        num = int(num)
        if num > 0:
            return True
        return False
    except ValueError:
        return False


@extend_schema_view(  # adding the custom filtering atributes to our openAPI doc
    list=server_list_docs
)
class ServerViewSet(viewsets.ViewSet):
    """
    View set for managing server data.
    """
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Server.objects.all()

    def get_view_name(self):
        """
        Returns the custom view name.
        """
        return "Server data"

    def list(self, request: Request) -> Response:
        """
        Returns a list of servers based on query parameters.

        Args:
        request (Request): The HTTP request object.

        Returns:
        A queryset of server filtered by the givern parameters.

        Raises:
        AuthenticationFailed: If the user is not authenticated and filtering by user or server ID is requested.
        ValidationError: If there are validation errors in the query parameters.

        Query Parameters:
        - `category` (str): Category name identifying the specific category to filter servers by.
        - `qty` (int): Quantity of the servers to be returned. Must be an int greater than 0.
        - `by_user` (bool): Defines if we want to filter servers by the user who is making the request. \
            'true' or 'false'.
        - `with_num_members` (bool): Defines if we want to add the number of members for the server. \
            Accepted values 'true' or 'false'.
        - `by_serverId` (UUID): Filtering server by its ID.

        Example:
        To retrieve up to 5 servers in category 'example_category' with the number of members:

            GET /api/servers/?category=example_category&with_num_members=true&qty=5

        To retrieve servers filtered by user with server ID '123e4567-e89b-12d3-a456-426614174000':

            GET /api/servers/?by_user=true&by_serverId=123e4567-e89b-12d3-a456-426614174000

        """
        # possible query parameters
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        with_num_members = request.query_params.get("with_num_members") == "true"
        by_serverId = request.query_params.get("by_serverId")

        queryset_filtered = self.get_queryset()

        # Ensure the user is authenticated if filtering by user or server ID
        if (by_user or by_serverId) and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            queryset_filtered = queryset_filtered.filter(
                category__name__iexact=category
            )

        if by_user:
            user_id = request.user.id
            # self.queryset = self.queryset.filter(member__id=user_id)
            queryset_filtered = queryset_filtered.filter(member=user_id)

        if with_num_members:
            queryset_filtered = queryset_filtered.annotate(num_members=Count("member"))

        if by_serverId:
            try:
                # Check if by_serverId is a valid UUID
                uuid.UUID(str(by_serverId))
                queryset_filtered = queryset_filtered.filter(id=by_serverId)
                # if the id does not exists
                if not queryset_filtered.exists():
                    raise ValidationError(
                        detail=f"Server with id: {by_serverId} does not exists."
                    )
            except ValueError:  # if the by_serverId is in wrong format
                raise ValidationError(
                    detail=f"The id: {by_serverId} is not in the right UUID format."
                )

        if qty:
            if not is_pos_int(qty):
                raise ValidationError(
                    detail=f"The qty: {qty} has to be a positive integer."
                )
            queryset_filtered = queryset_filtered[: int(qty)]

        serializer = ServerSerializer(
            queryset_filtered, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
