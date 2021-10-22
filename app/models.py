from __future__ import unicode_literals
from django.conf import settings
from datetime import datetime
import uuid
from django.db import models
from django.template.loader import render_to_string
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

from localflavor.us.us_states import STATE_CHOICES
from localflavor.us.models import USStateField
from django_pandas.managers import DataFrameManager
from . import choice

# Create your models here.
class location(models.Model):

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	major_city = models.CharField(max_length=255, null=True, blank=True, default="")
	county = models.CharField(max_length=255, null=True, blank=True, default="")
	state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
	fips_state = models.CharField(max_length=10, null=True, blank=True,default='')
	fips_county = models.CharField(max_length=10, null=True, blank=True,default='')
	zipcode = models.CharField(max_length=10, null=True, blank=True,default='')
	neighborhood = models.CharField(max_length=100, null=True, blank=True,default='')
	notes = models.TextField(null=True, blank=True,default='')
	population_served = models.IntegerField( blank=True, null=True, default = 0)
	created = models.DateTimeField( auto_now_add=True)

	def __unicode__(self):
		return '%s, %s' % ( self.major_city, self.state)

class data(models.Model):
	location =  models.ForeignKey(location, models.PROTECT)
	timestamp = models.DateTimeField( auto_now_add=True)
	year = models.IntegerField( blank=True, default = 0)
	quarter = models.CharField(max_length=10, null=True, blank=True, choices = choice.QUARTER,default='')
	score = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
	objects = DataFrameManager()

	def __unicode__(self):
		return '%s - %s' % (self.location.fips_county, self.timestamp)

	class Meta:
		verbose_name_plural = "Data"
