from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from webchat.serializers import MessageSerializer

message_list_docs = extend_schema(
    responses=MessageSerializer(many=True),
    parameters=[  # adding the custom filtering atributes to our openAPI doc
        OpenApiParameter(
            name="by_channelId",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.STR,
            description="ID of the channel, used to filter the messages.",
            required=True,
        ),
    ],
)
