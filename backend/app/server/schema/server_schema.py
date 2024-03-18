from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from server.serializers import ServerSerializer

server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[  # adding the custom filtering atributes to our openAPI doc
        OpenApiParameter(
            name="category",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.STR,
            description="category name idetyfing the specific category to filter servers by.",
        ),
        OpenApiParameter(
            name="qty",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.INT,
            description="quantity of the servers to be returned. Must be an int greater than 0.",
        ),
        OpenApiParameter(
            name="by_user",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.BOOL,
            description="defines if we want to filter servers by the user who is "
            + "making the request. 'true' or 'false'.",
        ),
        OpenApiParameter(
            name="by_serverId",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.UUID,
            description="Filtering server by it's ID.",
        ),
        OpenApiParameter(
            name="with_num_members",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.BOOL,
            description="defines if we want to add the number of members for the server."
            + "Accepted values 'true' or 'false'.",
        ),
    ],
)
