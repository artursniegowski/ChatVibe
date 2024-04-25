"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# TODO: set to production settings, use this file in production!
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# we need to make sure that this import is after the application has been generated
# so it has to come after DJANGO_SETTINGS_MODULE env variable
from . import urls  # noqa E402

# setting up the router so we can redirect http and websocket traffic
application = ProtocolTypeRouter(
    {
        # Django's ASGI application to handle traditional HTTP requests
        "http": django_asgi_app,
        # WebSocket handler
        "websocket": URLRouter(urls.websocket_urlpatterns),
    }
)
