from drf_spectacular.utils import extend_schema
from rest_framework import status

from utils.jwt_tokens.serializers import CustomTokenObtainPairSerializer

token_obtain_post_schema = extend_schema(
    request=CustomTokenObtainPairSerializer,
    responses={
        (status.HTTP_200_OK, "application/json"): {
            "description": "Set the access and refresh token successfully",
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                },
            },        
        },
        (status.HTTP_401_UNAUTHORIZED,  "application/json"): {
            "description": "Email and password dont match a user.",
            "type": "object",
            "properties": {
                "detail": {
                    "type": "string",
                    "example": "No active account found with the given credentials",
                },
            },
        },
        (status.HTTP_400_BAD_REQUEST,  "application/json"): {
            "description": "Email or password is missing in the body of the request.",
            "type": "object",
            "properties": {
                "email": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "password": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
            },
            "required": ["email", "password"],
            "example": {
                "email": ["This field is required."],
                "password": ["This field is required."]
            }
        },
    },
)
