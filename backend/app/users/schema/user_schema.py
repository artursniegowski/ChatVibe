from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema

from users.serializers import UserSerializer

user_list_docs = extend_schema(
    responses=UserSerializer,
    parameters=[  # adding the custom filtering atributes to our openAPI doc
        OpenApiParameter(
            name="by_userId",
            location=OpenApiParameter.QUERY,
            type=OpenApiTypes.STR,
            description="The ID of the user is used to filter the users and return one.",
            required=True,
        ),
    ],
)
