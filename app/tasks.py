from __future__ import absolute_import

from waterquality.celery import app
from app import models
from annoying.functions import get_object_or_None
from utils.log import log
from datetime import datetime, timedelta
from utils.crawlers.remote_water_quality_monitoring_network import remote_water_quality_monitoring_network


from app.const import (
	_SENSOR_UNITS
)

@app.task
def crawl_usgs_waterdata( daysago = 7):
	pass


@app.task
def remote_water_quality_monitoring_network_task():
	log('Running Remote Water Quality Monitoring Network Parser','info')
	crawler = remote_water_quality_monitoring_network()
	for node in crawler.get():
		station = get_object_or_None(models.node, name = node['station'])
		if not station:
			station = models.node()
			station.name = node['station']
			station.sourcetype = 'live'
			station.devicealias = node['station'].replace(' ','_').lower()
			station.save()
			log('Station: %s (%s) created' % (station.name, station.devicealias),'info')

		# insert sensor data
		for sensor_type, unit in _SENSOR_UNITS.iteritems():
			if sensor_type in ['orp']:
				continue

			data = models.data()
			data.source = station.sourcetype
			data.node_name = station.name
			data.node_alias =station.devicealias
			data.sensor_type = sensor_type
			data.sensor_units = unit
			data.lat = station.lat
			data.long = station.long

			if node[sensor_type]:
				data.value = round(float(node[sensor_type]), 2)
			else:
				data.value = 0.0

			data.save()
		log('Station: %s data updated' % (station.name),'info')
	log('Done','success')
