from .common import *

STATIC_ROOT = os.path.join(BASE_DIR, "static")

EMAIL_BACKEND = 'sgbackend.SendGridBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
SENDGRID_API_KEY = get_env_variable("SENDGRID_API_KEY",'')

sentry_sdk.init(
    dsn=get_env_variable('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()
    #, CeleryIntegration(), RedisIntegration(), TornadoIntegration()
    ],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
