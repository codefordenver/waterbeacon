
from __future__ import unicode_literals

from django.db import models
from .choice import (
    FEED_SOURCE,
    WATER_STATUS,
)
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from geopy.geocoders import Nominatim

# top us cities
# https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

class location(models.Model):
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True,default='')
    geocode = models.CharField(max_length=255, null=True, blank=True,default='')
    status = models.CharField(max_length=255, null=True, blank=True,choices=WATER_STATUS, default="info")
    keywords = models.CharField(max_length=255, null=True, blank=True,default='')
    created = models.DateTimeField( null=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        geolocator = Nominatim()
        geoc = geolocator.geocode("%s %s" % (self.city, self.state.lower() ), timeout=10)
        self.geocode = 'longitude=%s, latitude=%s, radius=5' % (geoc.latitude, geoc.longitude )
        return super(location, self ).save(*args, **kwargs)

	def __unicode__(self):
	    return '%s,%s' % (self.city,  self.state)

class tweet(models.Model):
    location = models.ForeignKey(location, null=True, blank=True)
    ignore = models.BooleanField(default=True)
    source = models.CharField(max_length=255, null=True, blank=True,default='')
    text = models.CharField(max_length=255, null=True, blank=True,default='')
    text_stopwords = models.TextField(null=True, blank=True,default='')

class url(models.Model):
    tweet = models.ForeignKey(tweet, null=True, blank=True)
    links = models.CharField(max_length=255, null=True, blank=True,default='')

class utility(models.Model):
    geocode = models.CharField(max_length=255, null=True, blank=True,default='')
    name  = models.CharField(max_length=255, null=True, blank=True,default='')
    link =  models.CharField(max_length=255, null=True, blank=True,default='')
    location = models.ForeignKey(location, null=True, blank=True)
    population =  models.IntegerField( blank=True, default = 0)
    violation = models.BooleanField(default=True)
    violation_points =  models.IntegerField( blank=True, default = 0)
    last_updated = models.DateTimeField(auto_now= True )
