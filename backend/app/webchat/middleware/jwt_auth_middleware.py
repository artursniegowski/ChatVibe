import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


@database_sync_to_async
def get_user(scope):
    token = scope["token"]
    if token is None:
        return AnonymousUser()
    secret_key_jwt = getattr(settings, "SIMPLE_JWT", {}).get(
        "SIGNING_KEY", settings.SECRET_KEY
    )
    try:
        token_payload = jwt.decode(token, secret_key_jwt, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    user_id = token_payload.get("user_id", None)
    if user_id is None:
        return AnonymousUser()
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


# the middlewre wil be called eveytime we try making a new web scoket connection
class JWTAuthMiddleWare:
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # grabing scope from header
        # exctracting cookies from the scope headers
        headers_dict = dict(scope["headers"])
        cookies = headers_dict.get(b"cookie", b"").decode("utf-8")
        cookies_dict = {
            item.split("=")[0]: item.split("=")[1] for item in cookies.split("; ")
        }
        access_toke_name = getattr(settings, "SIMPLE_JWT", {}).get(
            "JWT_AUTH_COOKIE_NAME", "access_token"
        )
        # refresh_token_name = getattr(settings, "SIMPLE_JWT", {}).get("JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token")
        access_toke = cookies_dict.get(access_toke_name, None)
        # refresh_token = cookies_dict.get(refresh_token_name)

        scope["token"] = access_toke
        scope["user"] = await get_user(scope)

        return await self.app(scope, receive, send)
