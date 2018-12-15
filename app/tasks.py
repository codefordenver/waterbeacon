from __future__ import absolute_import

from waterquality.celery import app
from app import models
from annoying.functions import get_object_or_None
from utils.log import log
from datetime import datetime, timedelta

from app.const import (
	_SENSOR_UNITS
)

@app.task
def crawl_usgs_waterdata( daysago = 7):
	pass
