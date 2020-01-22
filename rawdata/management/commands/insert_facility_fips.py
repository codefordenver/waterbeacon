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
        facilities = rawdata_models.EpaFacilitySystem.objects.all()
        fac_df = read_frame(facilities)

        water_systems = rawdata_models.EpaWaterSystem.objects.all()
        ws_df = read_frame(water_systems)

        completed = 0
        total = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = '').count()
        print('%s Facilities that need FIPs Codes' % (total))
        # update all facilities that do not have FIPSCodes
        for facility in rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = ''):
            fac_pws_id = facility.PWSId
            county_fips = ''
            equiv_ws_list = ws_df[(ws_df['PWSId'] == fac_pws_id)]
            if equiv_ws_list['id'].count() > 0:
                equiv_ws = equiv_ws_list.iloc[0]
                county_fips = equiv_ws['FIPSCodes']
            if county_fips == '':
                print('checking census block for %s' %fac_pws_id)
                county_fips = get_census_block(facility.FacLat, facility.FacLong )

            facility.FacFIPSCode = county_fips.split(', ')[0]
            facility.save()

        for __, facility in fac_df.iterrows():
            if not app_models.location.objects.filter(fips_county =  facility['FacFIPSCode']).exists():
                county_fips = facility['FacFIPSCode']
                location = app_models.location()
                location.fips_county = county_fips
                location.state = facility.FacState
                location.fips_state = state_fips[facility.FacState]
                location.county = facility.FacCounty
                fips_populations = ws_df[ws_df['FIPSCodes'] == facility['FacFIPSCode']]['PopulationServedCount'].sum()
                location.population_served = fips_populations

                if facility['FacFIPSCode'] in fips_to_zip:
                    location.zipcode = fips_to_zip[facility['FacFIPSCode']]
                    result = search.by_zipcode( location.zipcode )
                    location.major_city = result.major_city
                try:
                    location.save()
                except:
                    self.stdout.write('%s not saved' %location)

            completed +=1
            if completed % 100 == 0:
                total = rawdata_models.EpaFacilitySystem.objects.filter(FacFIPSCode = '').count()
                print('%s [%s]' % ( total , completed))
