import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from django.conf import settings
from uszipcode import SearchEngine
from app import models
from utils.log import log

class Command(BaseCommand):

    def xstr(self, s):
        if s is None:
            return ''
        return s.encode('ascii', errors='ignore').decode("utf-8")

    def handle(self, *args, **options):
        search = SearchEngine(simple_zipcode=True)
        baseDir  = settings.BASE_DIR
        with open('%s/app/management/commands/state_fips.json' % ( baseDir )) as json_file:
            state_fips = json.load(json_file)


        with open('%s/app/management/commands/zip2fips.json' % ( baseDir )) as json_file:
            zip2fips = json.load(json_file)

        for zip, fips_county in zip2fips.items():

            zip = self.xstr(zip)
            fips_county = self.xstr(fips_county)

            if not models.location.objects.filter(fips_county = fips_county).exists():
                location = models.location()
            else:
                #location = models.location.objects.filter(fips_county = fips_county).first()
                continue

            result = search.by_zipcode(zip)

            if result:
                location.county = result.county
                location.zipcode = zip
                location.state = result.state
                location.major_city = result.major_city

                location.fips_state = state_fips[result.state]

                location.fips_county = fips_county
                location.population = result.population
                location.population_density = result.population_density
                location.save()

                log('%s [%s]' % ( location.county, location.state ), 'success')
            else:
                log('%s [%s]' % ( zip, fips_county ), 'warning')
