from drf_spectacular.utils import extend_schema
from rest_framework import status


token_refresh_post_schema = extend_schema(
    # request=CustomTokenRefreshSerializer,
    request=None,
    responses={ 
        (status.HTTP_200_OK, "application/json"): {},
        (status.HTTP_401_UNAUTHORIZED,  "application/json"): {
            "description": "Refresh token wrong or missing.",
            "type": "object",
            "properties": {
                "detail": {
                    "type": "string",
                    "default": "Token is invalid or expired",
                },
                "code": {
                    "type": "string",
                    "default": "token_not_valid",
                },
            },
        }
    },
)
