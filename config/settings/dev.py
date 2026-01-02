
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# Dev tools có thể bật thêm
# INSTALLED_APPS += ["debug_toolbar"]

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}