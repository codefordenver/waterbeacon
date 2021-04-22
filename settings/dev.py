from .common import *

import os

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "waterbeacon",
        "USER": os.getenv("PG_USERNAME"),
        "PASSWORD": os.getenv("PG_PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,
    }
}

ENVIRONMENT = "dev"
USER = "Orange"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
