from django.contrib import admin
from news import models

# Register your models here.
def register_admin(model):
    """Turn admin.site.register into a decorator."""
    def wrapper(klass):
        admin.site.register(model, klass)
        return klass
    return wrapper

@admin.register(models.location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city','state','keywords')
    exclude = ('position',)

class URLInline(admin.TabularInline):
    model = models.url
    exclude = ()

@admin.register(models.advisory_feed)
class AdvisoryFeedAdmin(admin.ModelAdmin):
    list_display = ('source','feed',)

@admin.register(models.advisory_keyword)
class AdvisoryKeywordAdmin(admin.ModelAdmin):
    list_display = ('source','keyword',)

@admin.register(models.alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('sourceId','text','status','source','location','ignore')
    list_filter = ('ignore','source','created')
    inlines = [
    	URLInline,
    ]


class ServedInline(admin.TabularInline):
    model = models.county_served
    exclude = ()

@admin.register(models.utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ('name','has_contaminats','violation')
    inlines = [
    	ServedInline,
    ]
