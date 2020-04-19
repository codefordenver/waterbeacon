from datetime import datetime, timedelta

from waterquality.celery import app
from app import models
from annoying.functions import get_object_or_None
from utils.log import log

@app.task
def crawl_usgs_waterdata( daysago = 7):
	pass
