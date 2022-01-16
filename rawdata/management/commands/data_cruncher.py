import os, json
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_data_cruncher import ( SDW_Data_Cruncher )
from app import models as app_models
from rawdata import models as raw_models
from utils.log import log
from django_pandas.io import read_frame
import pandas as pd
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):

        now = timezone.now()
        year = now.year
        if now.month >= 11:
            quarter = 'q4'
        elif now.month >= 8:
            quarter = 'q3'
        elif now.month >= 5:
            quarter = 'q2'
        else:
            quarter = 'q1'


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
                # systems = raw_models.EpaFacilitySystem.objects.filter(FacFIPSCode = area['fips_county']).values()
                # systems_df = read_frame(systems)
                # if systems_df.shape[0] != 0:
                #     systems_df['in_violation'] = systems_df.apply(lambda x: x['CurrVioFlag']==1, axis=1)
                #     systems_df = systems_df[['PWSId', 'FacName', 'FacLong', 'FacLat', 'in_violation']]
                if area['score'] == 0:
                    if not app_models.data.objects.filter(location = location, score = area['score'], quarter = quarter, year = year).exists():
                        data = app_models.data()
                        data.year = year
                        data.quarter = quarter
                        data.location = location
                        data.score = area['score']
                        try:
                            data.save()
                            log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'success')
                        except:
                            print(location)
                    else:
                        log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'info')
                else:
                    location = app_models.location.objects.filter(fips_county =  area['fips_county']).first()
                    print(area.systems.head())
                    if area['score'] - 0.05 < 0:
                        min_score = 0
                    else:
                        min_score = area['score'] - 0.05
                    max_score = area['score'] + 0.05

                    if not app_models.data.objects.filter(location = location, score__gte = min_score, score__lte = max_score, quarter = quarter, year = year).exists():
                        data = app_models.data()
                        # todo: need to insert facilities here
                        data.location = location
                        data.quarter = quarter
                        data.location = location
                        data.score = area['score']
                        try:
                            data.save()
                            log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'success')
                        except:
                            print(location)
                    else:
                        log('%s, %s [%s]' % (location.major_city, location.state, area['score']), 'info')

            # save data rank
            prior_score = 0
            rank = 1
            for  data in app_models.data.objects.filter(quarter = quarter, year = year).order_by('score'):
                if data.score == prior_score:
                    data.rank = rank
                else:
                    rank += 1
                    data.rank = rank
                    prior_score = data.score
                data.save()
