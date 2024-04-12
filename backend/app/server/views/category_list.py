from drf_spectacular.utils import extend_schema_view
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from server.models import Category
from server.schema import category_list_docs
from server.serializers import CategorySerializer


@extend_schema_view(list=category_list_docs)  # definign the custom serializer
class CategoryViewSet(viewsets.ViewSet):

    def get_queryset(self):
        return Category.objects.all()

    def get_view_name(self):
        """
        Returns the custom view name.
        """
        return "Category data"

    def list(self, request: Request) -> Response:
        """
        Returns a list of categories.
        """
        serializer = CategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
