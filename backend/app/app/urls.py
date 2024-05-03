"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from channels.routing import URLRouter
from django.conf import settings

# from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from utils.jwt_tokens.views import (
    JWTCookieTokenObtainPairView,
    JWTCookieTokenRefreshView,
)
from webchat.ws_urls import urlpatterns as websocket_webchat_urlpatterns

urlpatterns = [
    # ## build in urls - START ## #
    path("admin/", admin.site.urls),
    # drf_spectacular - schema to download
    path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional GUI - spectacualr / swagger - documentation:
    path(
        "api/docs/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # token authentication
    path(
        "api/token/", JWTCookieTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", JWTCookieTokenRefreshView.as_view(), name="token_refresh"
    ),
    # ## build in urls - END ## #
    # ## custom urls - START ## #
    path("api/health/", include("core.urls")),
    path("api/", include("server.urls")),
    path("api/", include("webchat.urls")),
    path("api/", include("users.urls")),
    # ## custom urls - END ## #
]


if settings.DEBUG:
    # for serving files in development - only!!
    # not needed as media and static files served by nginx!
    # dont forget to run collectstatic to move all the static files!!
    # only needed if django service is accessed directly without nginx like
    # localhost:8000/api
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # debug toolbar active in debug only
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]


admin.site.site_header = "ChatVibe Dashboard Admin"
admin.site.site_title = "ChatVibe Admin Portal"
admin.site.index_title = "Welcome to ChatVibe Dashboard"


websocket_urlpatterns = [
    path("ws/", URLRouter(websocket_webchat_urlpatterns)),
]
