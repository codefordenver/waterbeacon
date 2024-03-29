import json
from django.core.management.base import BaseCommand
from django.conf import settings
from rawdata import models as rawdata_models
from app import models as app_models
from django.db.models import Sum
from django_pandas.io import read_frame

class Command(BaseCommand):

    def handle(self, *args, **options):
        total  = app_models.location.objects.filter(population_served = 0).count()
        print('total: %s' % ( total ))

        completed = 0

        location_water_systems = rawdata_models.EpaWaterSystem.objects.all()
        lws_df = read_frame(location_water_systems)
        fips_populations = lws_df.groupby(['FIPSCodes'])['PopulationServedCount'].sum()

        for location in app_models.location.objects.filter(population_served = 0):

            fips_county = str(int(float(location.fips_county)))
            if not location.fips_county or not fips_populations.get(fips_county, 0):
                print('location: %s skip' % (location.pk))
                continue

            location.population_served = fips_populations[fips_county]
            location.save()

            completed +=1
            if completed % 100 == 0:
                total  = app_models.location.objects.filter(population_served = 0).count()
                print('%s [%s]' % ( total , completed))
