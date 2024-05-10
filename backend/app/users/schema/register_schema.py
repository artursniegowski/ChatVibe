from drf_spectacular.utils import extend_schema
from rest_framework import status

from users.serializers import RegisterSerializer

register_post_docs = extend_schema(
    request=RegisterSerializer,
    responses={status.HTTP_201_CREATED: RegisterSerializer},
)
