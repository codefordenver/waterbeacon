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

import choice

import const

# Create your models here.
class node(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, null=True, blank=True,default='')
	position = models.PointField(null=True, blank=True)
	county = models.CharField(max_length=255, null=True, blank=True, default="")
	state = USStateField(choices=STATE_CHOICES, null=True, blank=True)
	fips_state = models.CharField(max_length=255, null=True, blank=True,default='')
	fips_county = models.CharField(max_length=255, null=True, blank=True,default='')
	source = models.CharField(max_length=255, null=True, blank=True,choices=choice.SOURCE_TYPE, default="usgs")
	score = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
	status = models.CharField(max_length=255, null=True, blank=True, choices= choice.NODE_STATUS ,default='')
	meta = JSONField()
	notes = models.TextField(null=True, blank=True,default='')
	created = models.DateTimeField( auto_now_add=True)


	def __unicode__(self):
		return self.name

	def _chart(self, sensor_type, title, label):
		out = []
		now = datetime.today()
		date = datetime.now() - settings.MAXIMUM_CHART_DAYS
		for datum in data.objects.filter(node = self,metric = sensor_type, timestamp__gte = date):
			out.append({
				'time':datum.timestamp,
				'value': int(datum.value)
				})

		return render_to_string('admin/app/node/chart.html', {'data':out,'chart_div':sensor_type,'title':title,'label':label,'units': const.SENSOR_UNITS[sensor_type] })

	def ph_chart(self):
		return self._chart('ph','Ph Chart','Ph')
	ph_chart.allow_tags = True

	def temperature_chart(self):
		return self._chart('temperature','Temperature Chart','Temperature')
	temperature_chart.allow_tags = True

	def conductivity_chart(self):
		return self._chart('conductivity','Conductivity Chart','Conductivity')
	conductivity_chart.allow_tags = True

	def turbidity_chart(self):
		return self._chart('turbidity','Turbidity Chart','Turbidity')
	turbidity_chart.allow_tags = True

	def orp_chart(self):
		return self._chart('orp','Oxygen Reduction Potential Chart','Oxygen Reduction Potential')
	orp_chart.allow_tags = True

	def odo_chart(self):
		return self._chart('odo','Dissolved Oxygen Chart','Dissolved Oxygen')
	odo_chart.allow_tags = True

class data(models.Model):
	node =  models.ForeignKey(node)
	timestamp = models.DateTimeField( auto_now_add=True)
	metrics = JSONField(null = True, blank = True)
	objects = DataFrameManager()

	def __unicode__(self):
		return '%s - %s (%s) ' % (self.node.name, self.timestamp)

	class Meta:
		verbose_name_plural = "Data"
