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

from app import choice
from app import const


class Address(models.Model):
    street_number = models.CharField(
        blank=True, default='', max_length=255, null=True)
    street_name = models.CharField(
        blank=True, default='', max_length=255, null=True)
    city = models.CharField(blank=True, default='', max_length=255, null=True)
    zipcode = models.CharField(
        blank=True, default='', max_length=10, null=True)
    county = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True)
    state = USStateField(choices=STATE_CHOICES, null=True, blank=True)


class FipsCode(models.Model):
    fips_code = models.CharField(max_length=15)


class Location(models.Model):
    score = models.DecimalField(decimal_places=3, default=0.0, max_digits=15)
    fips_code = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to='app.FipsCode')


class Facility(models.Model):
    FAC_TYPES = (('CWS', 'Community Water System'), ('OTHER', 'Other'))
    facility_name = models.CharField(max_length=255)
    pws_id = models.CharField(max_length=255, unique=True)
    registry_id = models.CharField(max_length=12, unique=True)
    current_violation_score = models.IntegerField(default=0)
    historic_violation_score = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    facility_type = models.CharField(choices=FAC_TYPES, max_length=255)
    population_served = models.IntegerField(
        blank=True, default=0, null=True)
    address_key = models.ForeignKey(
        blank=True, on_delete=models.CASCADE, to='app.Address')
    fips_code = models.ForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to='app.FipsCode')
