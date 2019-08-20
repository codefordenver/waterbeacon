import json
from django.core.management.base import BaseCommand
from django.conf import settings
from rawdata import models as rawdata_models
from app import models as app_models
from utils.utils import ( get_census_block )
from uszipcode import SearchEngine


class Command(BaseCommand):

    def handle(self, *args, **options):

        baseDir  = settings.BASE_DIR
        with open('%s/app/management/commands/state_fips.json' % ( baseDir )) as json_file:
            state_fips = json.load(json_file)

        with open('%s/app/management/commands/fips2zip.json' % ( baseDir )) as json_file:
            fips_to_zip = json.load(json_file)

        search = SearchEngine(simple_zipcode=True)

        completed = 0
        total = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = '').count()
        print('%s Facilities that need FIPs Codes' % (total))
        for facility in rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = ''):
            county_fips = get_census_block(facility.FacLat, facility.FacLong )

            facility.FacFIPSCode = county_fips
            facility.save()

            if not app_models.location.objects.filter(fips_county =  county_fips).exists():
                location = app_models.location()
                location.fips_county = county_fips
                location.state = facility.FacState
                location.fips_state = state_fips
                location.county = facility.FacCounty
                location.population_served = rawdata_models.EpaWaterSystem.objects.filter( FIPSCodes__contains = fips_code ).aggregate(Sum('PopulationServedCount'))['PopulationServedCount__sum']

                if county_fips in fips_to_zip:
                    location.zipcode = fips_to_zip[county_fips]
                    result = search.by_zipcode( location.zipcode )
                    location.major_city = result.major_city

                location.save()

            completed +=1
            if completed % 100 == 0:
                total = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = '').count()
                print('%s [%s]' % ( total , completed))
