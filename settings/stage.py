from .common import *
import raven

STATIC_ROOT = os.path.join(BASE_DIR, "static")

INSTALLED_APPS += ('raven.contrib.django.raven_compat',)
RAVEN_CONFIG = {
    'dsn': 'https://9bcdaac1c2fd4f2585ed55da4e97140b:71dfb078e8e241f19b91cbb9342df14b@app.getsentry.com/73520',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(BASE_DIR),
}

EMAIL_BACKEND = 'sgbackend.SendGridBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
SENDGRID_API_KEY = get_env_variable("SENDGRID_API_KEY",'')
