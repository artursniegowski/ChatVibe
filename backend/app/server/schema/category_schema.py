from drf_spectacular.utils import extend_schema

from server.serializers import CategorySerializer

category_list_docs = extend_schema(
    responses=CategorySerializer(many=True),
)
