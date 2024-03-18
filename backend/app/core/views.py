"""
Health Check of the web app
"""

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from core.schema import health_check_schema


@health_check_schema
@api_view(["GET"])
def health_check(request: Request) -> Response:
    """
    Returns a successful response indicating the health status of the application.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: A JSON response indicating the health status of the application.

    Examples:
        A successful response:
        {
            "status": "healthy"
        }
    """
    # TODO: add any relevant health checks as:
    # database queries, API checks, or any other checks relevant to your application's health # noqa
    return Response({"status": "healthy"})
