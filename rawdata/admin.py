# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rawdata.models import EpaFacilitySystem, EpaWaterSystem

from django.contrib import admin

# Register your models here.
admin.site.register(EpaFacilitySystem)
admin.site.register(EpaWaterSystem)
