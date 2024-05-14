from uuid import UUID

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from server.models import Server


# TODO: add the scheam for the views !!
class ServerMembershipViewSet(viewsets.ViewSet):
    """
    used to add and delete users as member for a spcifc channel
    """

    permission_classes = [IsAuthenticated]
    # to fix the issue:
    # Error [ServerMembershipViewSet]: unable to guess serializer
    serializer_class = None

    def create(self, request: Request, server_id: UUID) -> Response:
        """
        adding a user as a memebr to the given server
        """
        # getting the server
        server = get_object_or_404(Server, id=server_id)
        # getting th user tha makes the request
        user = request.user
        # checking if the user is a memeber of the server if not we add the user
        # as one
        if server.member.filter(pk=user.pk).exists():
            # if the users is alredy a member return an error response
            raise ValidationError(detail="User is already a member of the server.")

        # else
        # adding the user as a memebr to the server
        server.member.add(user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["DELETE"])
    def remove_member(self, request: Request, server_id: UUID) -> Response:
        """
        removing a user from the member group of the given server

        """
        # getting the server
        server = get_object_or_404(Server, id=server_id)
        # getting th user that makes the request
        user = request.user

        # making sure the owner of a server cant remove himself from
        # the members
        if server.owner == user:
            return Response(
                {"error": "Owners cannot be removed as a member"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # checking if the user is a memeber of the server if not we
        # return a validation error
        if server.member.filter(pk=user.pk).exists():
            # if the users is alredy a member we delete the user from the memebrship
            server.member.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # else
        # returnign validation error
        raise NotFound(detail="User is not a member of the server.")

    @action(detail=False, methods=["GET"])
    def is_member(self, request: Request, server_id: UUID) -> Response:
        """
        checking if a user is a memeber of the given server
        """
        # getting the server
        server = get_object_or_404(Server, id=server_id)
        # getting th user tha makes the request
        user = request.user

        is_member = server.member.filter(pk=user.pk).exists()

        return Response({"is_member": is_member})
