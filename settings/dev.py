from settings.common import * 

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'waterbeacon',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

ENVIRONMENT = 'dev'
USER='Orange'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

import djcelery
djcelery.setup_loader()
