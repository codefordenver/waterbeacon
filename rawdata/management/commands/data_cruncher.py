import os
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_data_cruncher import ( SDW_Data_Cruncher )
from app import models
from utils.log import log

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

            for area in areas:
                location = models.location.objects.filter(zipcode =  area['zipcode']).first()
                if area['score'] == 0:
                    if not models.data.objects.filter(location = location, score = score).exists():
                        data = models.data()
                        data.location = location
                        data.score = area['score']
                        data.save()
                        log('%s [%s]', )
                else:
                    if area['score'] - 0.05 < 0:
                        min_score = 0
                    else:
                        min_score = area['score'] - 0.05
                    max_score = area['score'] + 0.05
                if not models.data.objects.filter(location = location, score__gte = min_score, score__lte = max_score).exists():

                        data = models.data()
                        data.location = location
                        data.score = area['score']
                        data.save()
