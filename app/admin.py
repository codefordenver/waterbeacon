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

@admin.register(models.location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('state','county','notes')
    list_filter = ('state',)

@admin.register(models.data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('id','location','timestamp')
    list_filter = ('timestamp',)
