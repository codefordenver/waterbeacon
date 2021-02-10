from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'notifications', 'workshop', 'created', 'is_active')
    list_filter = ('is_active', 'notifications', 'workshop')
    search_fields = ('user__first_name', 'user__last_name')
