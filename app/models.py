from __future__ import unicode_literals
from django.conf import settings
from datetime import datetime
import uuid
from django.db import models
from django.template.loader import render_to_string

from .choice import (
	_COMM_TYPE,
	_SOURCE_TYPE,
	_SENSOR_TYPE
)

from .const import (
	_SENSOR_UNITS
)

class data(models.Model):
	timestamp = models.DateTimeField( auto_now_add=True)
	long = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True, blank=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, null=True, blank=True)
	source = models.CharField(max_length=255, null=True, blank=True,choices=_SOURCE_TYPE)
	value = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
	node_alias = models.CharField(max_length=255, null=True, blank=True,default='')
	node_name = models.CharField(max_length=255, null=True, blank=True,default='')
	sensor_name = models.CharField(max_length=255, null=True, blank=True,default='')
	sensor_type = models.CharField(max_length=255, null=True, blank=True,default='')
	sensor_units = models.CharField(max_length=255, null=True, blank=True,default='')
	def __unicode__(self):
	    return '%s - %s (%s) ' % (self.node_name, self.sensor_name, self.timestamp) 

# Create your models here.
class node(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	active = models.BooleanField(default=True)
	name = models.CharField(max_length=255, null=True, blank=True,default='')
	long = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	devicealias = models.CharField(max_length=255, null=True, blank=True,default='')
	sourcetype = models.CharField(max_length=255, null=True, blank=True,choices=_SOURCE_TYPE, default="sim")
	commtype = models.CharField(max_length=255, null=True, blank=True,choices=_COMM_TYPE)
	deviceaddress =models.CharField(max_length=255, null=True, blank=True,default='')
	hostip =models.CharField(max_length=255, null=True, blank=True,default='')
	proxy_url = models.CharField(max_length=255, null=True, blank=True,default='')
	notes = models.TextField(null=True, blank=True,default='')
	created = models.DateTimeField( auto_now_add=True)

	def __unicode__(self):
	    return self.name

	def _chart(self, sensor_type, title, label):
		out = []
		now = datetime.today()
		date = datetime.now() - settings.MAXIMUM_CHART_DAYS
		for datum in data.objects.filter(sensor_type = sensor_type, node_alias = self.devicealias, timestamp__gte = date):
			out.append({
				'time':datum.timestamp,
				'value': int(datum.value)
				})

		return render_to_string('admin/app/node/chart.html', {'data':out,'chart_div':sensor_type,'title':title,'label':label,'units':_SENSOR_UNITS[sensor_type] })

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


class tag(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True,default='')
	node = models.ForeignKey(node)

	def __unicode__(self):
	    return self.name

class sensor(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True,default='')
	type = models.CharField(max_length=255, null=True, blank=True,choices=_SENSOR_TYPE)
	mean = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
	std = models.DecimalField(max_digits=15, decimal_places=3, default=0.0)
	
	def __unicode__(self):
		return self.name

	@property
	def units(self):
		return _SENSOR_UNITS[self.type]



class sim_node(models.Model):
	active = models.BooleanField(default=True)
	name = models.CharField(max_length=255, null=True, blank=True,default='')
	devicealias = models.CharField(max_length=255, null=True, blank=True,default='')
	sensors = models.ManyToManyField(sensor)

	def __unicode__(self):
	    return self.name

	@property
	def measurement_count(self):
		sensor_count = self.sensors.all().count()
		total_measurement_count = data.objects.filter(node_alias = self.devicealias).count() 
		if sensor_count:
			return total_measurement_count / sensor_count
		return 0