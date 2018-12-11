
from __future__ import unicode_literals

from django.contrib.gis.db import models
from .choice import (
    FEED_SOURCE,
    WATER_STATUS,
)
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField


# top us cities
# https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

class location(models.Model):
    position = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True,default='')
    status = models.CharField(max_length=255, null=True, blank=True,choices=WATER_STATUS, default="info")
    keywords = models.CharField(max_length=255, null=True, blank=True,default='')
    created = models.DateTimeField( null=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        pass

	def __unicode__(self):
	    return '%s,%s' % (self.city,  self.state)

class tweet(models.Model):
    location = models.ForeignKey(location, null=True, blank=True)
    ignore = models.BooleanField(default=True)
    source = models.CharField(max_length=255, null=True, blank=True,default='')
    text = models.CharField(max_length=255, null=True, blank=True,default='')
    text_wo_stopwords = models.TextField(null=True, blank=True,default='')

class url(models.Model):
    tweet = models.ForeignKey(tweet, null=True, blank=True)
    links = models.CharField(max_length=255, null=True, blank=True,default='')

class utility(models.Model):
    name  = models.CharField(max_length=255, null=True, blank=True,default='')
    link =  models.CharField(max_length=255, null=True, blank=True,default='')
    has_contaminats =  models.BooleanField(default=True)
    position = models.PointField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True,default='')
    last_updated = models.DateTimeField(auto_now= True )

class violation(models.Model):
    utility =  models.ForeignKey(utility)
    text = models.CharField(max_length=255, null=True, blank=True,default='')
