import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_data_cruncher import ( SDW_Data_Cruncher )
from app import models as app_models
from rawdata import models as raw_models
from utils.log import log
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        cruncher = SDW_Data_Cruncher()

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
            for __, area in areas.iterrows():
                location = app_models.location.objects.filter(fips_county =  area['county_fips']).first()

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
