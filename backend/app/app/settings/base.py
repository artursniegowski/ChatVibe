"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# so if DEBUG is 1 = True, and if DEBUG is 0 = False
DEBUG = bool(int(os.environ.get("DJANGO_DEBUG", 0)))

# accessible only via specific host name
# so you want to make sure only that hostname can be used because otherwise
# it can open your applciation for certain vulnerabilities
# we will accept a comma seperated list and we will add all of them
# bc there can be many
ALLOWED_HOSTS = []
# so we are getting all the hosts, and if it dosent exists we will set an emty value ''
# next we are spliting everything by a coma, so many hosts can be defined with a coma,
# and filter out all the None vals,
# so basicaly if the list is empty the filter function will return empty list
# and extedn will not add anything to the empty list, otherwise we add all the hosts
ALLOWED_HOSTS.extend(
    filter(
        None,
        # retrived from the docker-composer ENV variables
        os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(","),
    )
)


# Application definition

INSTALLED_APPS = [
    # django apps - START
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # django apps - END
    # Local/custom apps - START
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "server.apps.ServerConfig",
    "webchat.apps.WebchatConfig",
    # Local/custom apps - END
    # third party apps - START
    "drf_spectacular",
    "rest_framework",
    "corsheaders",
    # third party apps - END
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.get_current_year_context",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # these settings are retrived from the docker-composer ENV variables
        "HOST": os.environ.get("POSTGRES_DB_HOST"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        # not specifying the port number -> Django will use the default
        # port number for PostgreSQL databse which is 5432
        # 'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# Using Argon2 with Django
# https://docs.djangoproject.com/en/5.0/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/static/"
MEDIA_URL = "static/media/"

# $ python manage.py collectstatic
# This will copy all files from your static folders into the STATIC_ROOT
# directory.

STATIC_ROOT = "/vol/web/static"
MEDIA_ROOT = "/vol/web/media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# update Django settings to use the custom user model
AUTH_USER_MODEL = "users.User"

# rest framework settings
REST_FRAMEWORK = {
    # register our spectacular AutoSchema with DRF
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # https://www.django-rest-framework.org/api-guide/settings/#default_authentication_classes
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # changeed to JWT tokens authentication - http only cookie !
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "utils.jwt_tokens.authentication.JWTCookieAuthentication",
    ],
    # AllowAny is set by defaul
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.IsAuthenticated",
    # ],
}

# adjusting settings for simplejwt
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html?highlight=SIGNING_KEY#settings
SIMPLE_JWT = {
    "SIGNING_KEY": os.environ.get("SIMPLE_JWT_SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "utils.jwt_tokens.serializers.CustomTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "utils.jwt_tokens.serializers.CustomTokenRefreshSerializer",
    # custom settings SIMPLE_JWT - START
    # JWT Cookies - custom settings for the JWTSetCookieMixin
    "JWT_AUTH_COOKIE_NAME": "access_token",  # setting the cookie name for the JWT authentication
    "JWT_AUTH_REFRESH_COOKIE_NAME": "refresh_token",
    "JWT_AUTH_SAMESITE": "Lax",
    # custom settings SIMPLE_JWT - END
}


# https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation
SPECTACULAR_SETTINGS = {
    "TITLE": "ChatVibe API",
    "DESCRIPTION": "The application aims to provide a platform for users to engage in real-time chat "
    + "conversations within categorized servers and channels, similar to popular platforms like Discord.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
    "SWAGGER_UI_SETTINGS": {
        # sets the access_token cookie, which needs to be delete manualy
        # after it expires - we will get a 401-unauthorized when accessing
        # the swagger-UI,
        # we get get a new token by posting email and passsword to
        # /api/token/  , this will set both refresh and access token,
        # then we either set this again in the authorization, or just keep it
        # in the cookie
        "persistAuthorization": True,
        "withCredentials": True,
    },
}


# configuration for channel layers
# https://channels.readthedocs.io/en/latest/topics/channel_layers.html#configuration
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Redis service name is 'redis'!
            # and the redis database runs on port 6379/1
            "hosts": [
                {
                    "host": os.environ.get("CHANNEL_LAYERS_REDIS_HOST"),
                    "port": os.environ.get("CHANNEL_LAYERS_REDIS_PORT"),
                    # set to 1 - can be adjusted
                    "db": os.environ.get("CHANNEL_LAYERS_REDIS_DB_INDEX"),
                }
            ],
        },
    },
}
