from django.conf import settings
from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension


# this works only partialy, it still sets the cookie, but also using
# localstorage, delete manulay the access token to get rid of 401
# if the token expires or is invalid
# https://github.com/swagger-api/swagger-ui/issues/9710
class JWTCookieOpenApiAuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = "utils.jwt_tokens.authentication.JWTCookieAuthentication"
    name = "JWTCookieAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": getattr(settings, "SIMPLE_JWT", {}).get(
                "JWT_AUTH_COOKIE_NAME", "access_token"
            ),
            "description": _(
                "JWT token-based authentication using HTTP-only cookies. "
                'The access token is stored in the "{}" cookie '
                'and the refresh token is stored in the "{}" cookie.'
            ).format(
                getattr(settings, "SIMPLE_JWT", {}).get(
                    "JWT_AUTH_COOKIE_NAME", "access_token"
                ),
                getattr(settings, "SIMPLE_JWT", {}).get(
                    "JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token"
                ),
            ),
        }
