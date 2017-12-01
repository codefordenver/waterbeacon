from __future__ import unicode_literals

from django.db import models
from .choice import (
    FEED_SOURCE,
    WATER_STATUS,
    CITY
)

# top us cities
# https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

class location(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True,choices=CITY, default="info")
    status = models.CharField(max_length=255, null=True, blank=True,choices=WATER_STATUS, default="info")
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    geocode = models.CharField(max_length=255, null=True, blank=True,default='')
    keywords = models.CharField(max_length=255, null=True, blank=True,default='')
    created = models.DateTimeField( null=True, auto_now_add=True)

class tweet(models.Model):
    location = models.ForeignKey(location, null=True, blank=True)
    ignore = models.BooleanField(default=True)
    source = models.CharField(max_length=255, null=True, blank=True,default='')
    text = models.CharField(max_length=255, null=True, blank=True,default='')
    text_stopwords = models.TextField(null=True, blank=True,default='')

class url(models.Model):
    tweet = models.ForeignKey(tweet, null=True, blank=True)
    links = models.CharField(max_length=255, null=True, blank=True,default='')
