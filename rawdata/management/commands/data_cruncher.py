import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_data_cruncher import ( SDW_Data_Cruncher )
from app import models as app_models
from rawdata import models as raw_models
from utils.log import log
from uszipcode import SearchEngine

class Command(BaseCommand):
    def handle(self, *args, **options):
        cruncher = SDW_Data_Cruncher()
        search = SearchEngine(simple_zipcode=True)

        baseDir  = settings.BASE_DIR
        with open('%s/app/management/commands/state_fips.json' % ( baseDir )) as json_file:
            state_fips = json.load(json_file)

        states = [
             "AL",  "AK",  "AS",  "AZ",  "AR",  "CA",  "CO",  "CT",
             "DE",  "DC",  "FM",  "FL",  "GA",  "GU",  "HI",  "ID",
             "IL",  "IN",  "IA",  "KS",  "KY",  "LA",  "ME",  "MH",
             "MD",  "MA",  "MI",  "MN",  "MS",  "MO",  "MT",  "NE",
             "NV",  "NH",  "NJ",  "NM",  "NY",  "NC",  "ND",  "MP",
             "OH",  "OK",  "OR",  "PW",  "PA",  "PR",  "RI",  "SC",
             "SD",  "TN",  "TX",  "UT",  "VT",  "VI",  "VA",  "WA",
             "WV",  "WI",  "WY"
        ]

        for state in states:

            areas = cruncher.calc_state_scores(state, print_test = True)
            for area in areas:
                location = app_models.location.objects.filter(zipcode =  area['zipcode']).first()
                if not location:
                    result = search.by_zipcode(area['zipcode'])
                    if raw_models.EpaFacilitySystem.objects.filter( FacZip = area['zipcode'] ).exists() and result:
                        facility = raw_models.EpaFacilitySystem.objects.filter( FacZip = area['zipcode'] ).first()
                        location = app_models.location()


                        location.county = facility.FacCounty
                        location.zipcode = facility.FacZip
                        location.state = facility.FacState
                        location.major_city = result.major_city
                        location.fips_state = state_fips[result.state]
                        location.fips_county = facility.FacFIPSCode
                        location.population = result.population
                        location.population_density = result.population_density
                        location.save()

                        log('zipcode: %s found and inserted' %( area['zipcode'] ), 'warning')
                    else:
                        log('zipcode: %s not found' %( area['zipcode'] ), 'error')
                    continue
                if area['score'] == 0:
                    if not app_models.data.objects.filter(location = location, score = area['score']).exists():
                        data = app_models.data()
                        data.location = location
                        data.score = area['score']
                        data.save()
                        log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'success')
                    else:
                        log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'info')
                else:
                    if area['score'] - 0.05 < 0:
                        min_score = 0
                    else:
                        min_score = area['score'] - 0.05
                    max_score = area['score'] + 0.05

                    if not app_models.data.objects.filter(location = location, score__gte = min_score, score__lte = max_score).exists():

                            data = app_models.data()
                            data.location = location
                            data.score = area['score']
                            data.save()
                            log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'success')
                    else:
                        log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'info')
