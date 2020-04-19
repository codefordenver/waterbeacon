import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default=None):
    try:
        return os.environ[var_name]
    except KeyError:
        return default


def get_env_variable_required(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
