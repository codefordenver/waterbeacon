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

@admin.register(models.node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('name','state','county','source','notes')
    search_fields = ['name']
    list_filter = ('state',)

#    readonly_fields = ('ph_chart', 'temperature_chart','conductivity_chart','turbidity_chart','orp_chart','odo_chart')
#    fieldsets = [
#            ('Node', { 'fields':  [  'active', 'name', 'long', \
#                            'lat', 'devicealias', 'sourcetype','commtype','deviceaddress','hostip','proxy_url','notes' ]}), \
#            ('Ph', { 'fields':  [  'ph_chart',  ]}),
#            ('Temperature', { 'fields':  [  'temperature_chart',  ]}),
#
#            ('Conductivity', { 'fields':  [  'conductivity_chart',  ]}),
#            ('Turbidity', { 'fields':  [  'turbidity_chart',  ]}),
#            ('Oxygen Reduction Potential', { 'fields':  [  'orp_chart',  ]}),
#            ('Dissolved Oxygen', { 'fields':  [  'odo_chart',  ]}),
#    ]

#    class Media:
#        js = ("js/node.js",)


@admin.register(models.data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('id','node','timestamp')
    list_filter = ('timestamp',)
