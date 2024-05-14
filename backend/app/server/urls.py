"""
Urls mappings for the server app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server import views

# this will generate the endpoints for servers
router = DefaultRouter(trailing_slash=False)
router.register("servers", views.ServerViewSet, basename="server")
router.register(
    "servers/categories", views.CategoryViewSet, basename="category"
)  # Register CategoryViewSet
router.register(
    # server_id need to have an uuid patern
    r"servers/membership/(?P<server_id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/membership",
    views.ServerMembershipViewSet,
    basename="membership",
)  # Register ServerMembershipViewSet


app_name = "server"

urlpatterns = [
    # ex: "api/"
    path("", include(router.urls)),
]
