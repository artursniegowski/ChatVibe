from drf_spectacular.utils import extend_schema

health_check_schema = extend_schema(
    description="Returns a successful response indicating the health status of the application.",
    responses={
        (200, "application/json"): {
            "description": "Success",
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "default": "healthy",
                },
            },
        },
    },
)
