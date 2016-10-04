from common import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ENVIRONMENT = 'dev'
USER='Orange'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

import djcelery
djcelery.setup_loader()
