"""Settings for local - development environment"""

import socket

from .base import *  # noqa

# Application definition

INSTALLED_APPS += [
    # third party apps
    "debug_toolbar",
]

### configuration for the debug toolbar ###
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
MIDDLEWARE.insert(0,"debug_toolbar.middleware.DebugToolbarMiddleware")
# Configure Internal IPs
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips  # noqa
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "10.0.2.2",
    ]
    # Adding IP addresses dynamically based on the local machine's hostname
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]
### configuration for the debug toolbar END ###
