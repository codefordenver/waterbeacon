from django.contrib import admin
from news import models
from admin_auto_filters.filters import AutocompleteFilter

# Register your models here.
def register_admin(model):
    """Turn admin.site.register into a decorator."""
    def wrapper(klass):
        admin.site.register(model, klass)
        return klass
    return wrapper

class LocationFilter(AutocompleteFilter):
    title = 'Location' # display title
    field_name = 'location' # name of the foreign key field

@admin.register(models.location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city','state','keywords')
    list_filter = ('status', )
    search_fields = [ 'city', 'state', 'county']
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

def safe(modeladmin, request, queryset):
    for alert in queryset:
        alert.status = 'safe'
        alert.save()

safe.short_description = 'Set Safe for Consumption status'

def notdrink(modeladmin, request, queryset):
    for alert in queryset:
        alert.status = 'notdrink'
        alert.save()
notdrink.short_description = 'Set Do Not Drink status'

def boil(modeladmin, request, queryset):
    for alert in queryset:
        alert.status = 'boil'
        alert.save()
boil.short_description = 'Set Boil Water status'

def notuse(modeladmin, request, queryset):
    for alert in queryset:
        alert.status = 'notuse'
        alert.save()
notuse.short_description = 'Set Do Not Use status'

@admin.register(models.alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('sourceId','text','status','source','location','published','ignore')
    list_filter = ('ignore','source','status','created','published')
    inlines = [
    	URLInline,
    ]
    list_filter = [LocationFilter]
    actions = [safe, notdrink, boil, notuse]

class ServedInline(admin.TabularInline):
    model = models.county_served
    exclude = ()

@admin.register(models.utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ('name','has_contaminats','violation')
    list_filter = ('has_contaminats','violation')
    search_fields = ['name', 'city', 'state']
    inlines = [
    	ServedInline,
    ]
