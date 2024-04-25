"""
urls for the webchat web socket
"""

from django.urls import path

from webchat.consumers import WebChatConsumer

app_name = "ws-webchat"

urlpatterns = [
    # ex: ws/
    path("<str:server_id>/<str:channel_id>/", WebChatConsumer.as_asgi()),
]
