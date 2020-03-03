from django.contrib import admin
from app import models
from utils.log import log
from copy import deepcopy
# Register your models here.

def register_admin(model):
    """Turn admin.site.register into a decorator."""
    def wrapper(klass):
        admin.site.register(model, klass)
        return klass
    return wrapper
    