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
    list_display = ('city','status','zipcode')


@admin.register(models.twitter_search)
class TwitterSearchAdmin(admin.ModelAdmin):
    list_display = ('title','location','active')
    list_filter = ('active',)

class URLInline(admin.TabularInline):
    model = models.url
    exclude = ()

@admin.register(models.tweet)
class TweetAdmin(admin.ModelAdmin):
    list_displat = ('text','source','ignore','account')
    list_filter = ('ignore',)
    inlines = [
    	URLInline,
    ]
