from common import *
import raven

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': 'aquauser',
        'PASSWORD': 'gQ&*Fk!WJp5z',
        'HOST': 'localhost',   
        'PORT': '5432',   
    }
}

STATIC_ROOT = '/home/aquauser/statics/' 
MEDIA_ROOT = '/home/aquauser/waterquality/media/' 
INSTALLED_APPS += ('raven.contrib.django.raven_compat',)

RAVEN_CONFIG = {
    'dsn': 'https://9bcdaac1c2fd4f2585ed55da4e97140b:71dfb078e8e241f19b91cbb9342df14b@app.getsentry.com/73520',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}

ENVIRONMENT = 'test'
USER='aquauser'

import djcelery
djcelery.setup_loader()

DEBUG = False