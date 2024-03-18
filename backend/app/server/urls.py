"""
Urls mappings for the server app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server import views

# this will generate the endpoints for servers
router = DefaultRouter(trailing_slash=False)
router.register("servers", views.ServerViewSet, basename="server")


app_name = "server"

urlpatterns = [
    # ex: "api/"
    path("", include(router.urls)),
]
