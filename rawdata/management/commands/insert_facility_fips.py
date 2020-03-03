import json
from django.core.management.base import BaseCommand
from django.conf import settings
from rawdata import models as rawdata_models
from app import models as app_models
from utils.utils import ( get_census_block )
from uszipcode import SearchEngine
from django_pandas.io import read_frame

class Command(BaseCommand):

    def handle(self, *args, **options):

        baseDir  = settings.BASE_DIR
        with open('%s/app/management/commands/state_fips.json' % ( baseDir )) as json_file:
            state_fips = json.load(json_file)

        with open('%s/app/management/commands/fips2zip.json' % ( baseDir )) as json_file:
            fips_to_zip = json.load(json_file)

        search = SearchEngine(simple_zipcode=True)

        ws_df = read_frame(rawdata_models.EpaWaterSystem.objects.all())

        facilities_without_fips = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = '')

        completed = 0
        total_facility_cnt = facilities_without_fips.count()

        self.stdout.write('%s facilities need FIPs Codes' %
                          (total_facility_cnt))

        # update all facilities that do not have FIPSCodes
        for facility in facilities_without_fips:
            county_fips = ''
            equiv_ws_list = ws_df[(ws_df['PWSId'] == facility.PWSId)]
            if equiv_ws_list['id'].count() > 0:
                equiv_ws = equiv_ws_list.iloc[0]
                county_fips = equiv_ws['FIPSCodes']
            if not county_fips:
                county_fips = get_census_block(facility.FacLat, facility.FacLong )

            # TODO I'm seeing values like 53342.0 and 53342
            facility.FacFIPSCode = county_fips.split(', ')[0]
            facility.save()

            completed +=1
            if completed % 100 == 0:
                self.stdout.write('Remaining: %s Completed: %s' %
                      (total_facility_cnt - completed, completed))

        facilites = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode__isnull=False).distinct(
            'FacFIPSCode')

        num_unique_fips = facilites.count()
        completed = 0

        self.stdout.write('Checking which facilities to add to locations. %s facilities.' % num_unique_fips)

        for facility in facilites:
            completed += 1
            if not app_models.location.objects.filter(fips_county=facility.FacFIPSCode).exists():
                county_fips = facility.FacFIPSCode
                location = app_models.Location()
                location.fips_county = county_fips
                location.state = facility.FacState
                location.fips_state = state_fips[facility.FacState]
                location.county = facility.FacCounty
                fips_populations = ws_df[ws_df['FIPSCodes'] == facility.FacFIPSCode]['PopulationServedCount'].sum()
                location.population_served = fips_populations

                if facility.FacFIPSCode in fips_to_zip:
                    location.zipcode = fips_to_zip[facility.FacFIPSCode]
                    result = search.by_zipcode( location.zipcode )
                    location.major_city = result.major_city
                try:
                    location.save()
                except:
                    self.stdout.write('%s not saved' %location)

            if completed % 100 == 0:
                self.stdout.write('Remaining: %s Completed: %s' %
                                  (num_unique_fips - completed, completed))
