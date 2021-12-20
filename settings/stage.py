from .common import *

STATIC_ROOT = os.path.join(BASE_DIR, "static")

sentry_sdk.init(
    dsn=get_env_variable('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()
    #, CeleryIntegration(), RedisIntegration(), TornadoIntegration()
    ],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
