
from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "uat.example.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "uat_db",
        "USER": "uat_user",
        "PASSWORD": "uat_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

SECURE_SSL_REDIRECT = False
