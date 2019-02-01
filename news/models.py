
from __future__ import unicode_literals

from django.contrib.gis.db import models
from .choice import (
    WATER_STATUS,
    SOURCE
)
from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField


# top us cities
# https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

class location(models.Model):
    position = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    county = models.CharField(max_length=255, null=True, blank=True, default="")
    state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True,default='')
    fips_state = models.CharField(max_length=255, null=True, blank=True,default='')
    fips_county = models.CharField(max_length=255, null=True, blank=True,default='')
    geocode = models.CharField(max_length=255, null=True, blank=True,default='')
    keywords = models.CharField(max_length=255, null=True, blank=True,default='')
    status = models.CharField(max_length=255, null=True, blank=True,choices=WATER_STATUS, default="safe")
    created = models.DateTimeField( null=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        geolocator = Nominatim()
        geoc = geolocator.geocode("%s %s" % (self.city, self.state.lower() ), timeout=10)
        self.geocode = 'longitude=%s, latitude=%s, radius=5' % (geoc.latitude, geoc.longitude )
        return super(location, self ).save(*args, **kwargs)

    def __unicode__(self):
        return '%s,%s' % (self.city,  self.state)

class advisory_feed(models.Model):
    source = models.CharField(max_length=255, null=True, blank=True,choices=SOURCE, default="")
    feed = models.CharField(max_length=255, null=True, blank=True,default='')

    def __unicode__(self):
        return self.feed

    class Meta:
        verbose_name_plural = "Advisory Feeds"
        verbose_name = "Advisory Feed"

class advisory_keyword(models.Model):
    source = models.CharField(max_length=255, null=True, blank=True,choices=SOURCE, default="")
    keyword = models.CharField(max_length=255, null=True, blank=True,default='')

    def __unicode__(self):
        return self.keyword

    class Meta:
        verbose_name_plural = "Advisory Keywords"
        verbose_name = "Advisory Keyword"

class alert(models.Model):
    location = models.ForeignKey(location, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True,choices=SOURCE, default="")
    sourceId = models.CharField(max_length=255, null=True, blank=True, default="")
    status = models.CharField(max_length=255, null=True, blank=True,choices=WATER_STATUS, default="safe")
    ignore = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True,default='')
    text_wo_stopwords = models.TextField(null=True, blank=True,default='')
    published = models.DateTimeField( null=True, blank = True )
    created = models.DateTimeField( null=True, auto_now_add=True)

    def __unicode__(self):
        return self.sourceId

class url(models.Model):
    alert = models.ForeignKey(alert, null=True, blank=True)
    link = models.TextField(null=True, blank=True,default='')

class utility(models.Model):
    name  = models.CharField(max_length=255, null=True, blank=True,default='')
    people_served = models.IntegerField( blank=True, default = 0)
    link =  models.CharField(max_length=255, null=True, blank=True,default='')
    has_contaminats =  models.BooleanField(default=True)
    position = models.PointField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True, default="")
    state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True,default='')
    fips_state = models.CharField(max_length=255, null=True, blank=True,default='')
    fips_county = models.CharField(max_length=255, null=True, blank=True,default='')
    violation = models.BooleanField(default=False)
    voilation_points = models.IntegerField( blank=True, default = 0)
    last_updated = models.DateTimeField(auto_now= True )

    class Meta:
        verbose_name_plural = "Utilities"

class county_served(models.Model):
    utility = models.ForeignKey(utility, null=True, blank=True)
    location = models.ForeignKey(location, null=True, blank=True)
