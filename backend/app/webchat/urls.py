"""
urls for the webchat
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from webchat import views

# this will generate the endpoints for servers
router = DefaultRouter(trailing_slash=False)
router.register("messages", views.MessageViewSet, basename="webchat-messages")

app_name = "webchat"

urlpatterns = [
    # ex: api/
    path("", include(router.urls)),
]
