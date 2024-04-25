from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from webchat.models import Conversation, Message
from webchat.schema import message_list_docs
from webchat.serializers import MessageSerializer


@extend_schema_view(  # adding the custom filtering atributes to our openAPI doc
    list=message_list_docs
)
class MessageViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Message.objects.all()

    def get_view_name(self):
        """
        Returns the custom view name.
        """
        return "Returns Messages data"

    def list(self, request: Request) -> Response:
        """
        Returns a list of messages based on query parameters.

        Args:
        request (Request): The HTTP request object.

        Returns:
        A queryset of messages filtered by the given parameters.

        Query Parameters:
        - `by_channelId` (str): It is required. Channel ID used to fillter all \
            the messages related to this specific channel.

        Example:
        To retrieve messages related to the channel with the id '550e8400-e29b-41d4-a716-446655440000':

            GET /api/messages&by_channelId=550e8400-e29b-41d4-a716-446655440000

        """
        by_channelId = request.query_params.get("by_channelId")

        if not by_channelId:
            raise ValidationError(detail="by_channelId parameter is required.")

        try:
            conversation = Conversation.objects.get(channel_id=by_channelId)
        except ValueError:
            raise ValidationError(
                detail=f"Channel ID: {by_channelId} is not in the right format."
            )
        except Conversation.DoesNotExist:
            messages = Message.objects.none()
        else:
            messages = conversation.message.all()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
