from drf_spectacular.utils import extend_schema
from rest_framework import status

logout_post_docs = extend_schema(
    responses={status.HTTP_200_OK: {"description": "Logged out successfully"}},
    # specify that there is no request body (serializer)
    request=None,
)
