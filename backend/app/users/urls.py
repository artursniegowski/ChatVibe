"""
Urls mappings for the users app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

# this will generate the endpoints for servers
router = DefaultRouter(trailing_slash=False)
router.register("user", views.UserViewSet, basename="user")

app_name = "users"

urlpatterns = [
    # ex: "api/"
    path("", include(router.urls)),
    path("logout/", views.LogOutAPIView.as_view(), name="logout"),
]
