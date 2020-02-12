from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Count
from django.http import Http404

from datetime import datetime, timedelta

from app import models as app_models
from news import models as news_models
from rawdata import models as raw_models
from django_pandas.io import read_frame
from utils.utils import ( str2bool )
import math


class locationData(APIView):
    # /v1/data/?sources=locations


    def get(self, request):
        response = {"meta":{ "cities": 0, "utilities": 0, "locations": 0, "facilities": 0},"locations":[], "utilities" :[], 'cities':[], 'facilities': []}

        sources = request.query_params.get('sources','').split(',')


        # filter for locations
        if 'locations' in sources or not len(sources):

            queryset = app_models.location.objects.all()
            facilities_rd = raw_models.EpaFacilitySystem.objects.all()
            fac_df = read_frame(facilities_rd)
            fac_df = fac_df[fac_df['CurrVioFlag'] == 1]
            fac_df = fac_df[[
                'FacFIPSCode',
                'PWSId',
                'FacName',
                'FacLong',
                'FacLat'
            ]]
            total_facilities = 0
            for location in queryset:
                if app_models.data.objects.filter(location = location, score__gt=0).exists():
                    # get facilities
                    facilities = []
                    for facility in fac_df[fac_df['FacFIPSCode'] == location.fips_county].itertuples():
                        total_facilities += 1
                        facilities.append({
                            'PWSId': facility.PWSId,
                            'FacName': facility.FacName,
                            'long':facility.FacLong,
                            'lat': facility.FacLat,
                        })

                    total_facilities += len(facilities)
                    data = app_models.data.objects.filter(location = location, score__gt=0).latest('timestamp')

                    if math.isnan(data.score):
                        response["locations"].append({
                            "fips_state_id": location.fips_state,
                            "fips_county_id": location.fips_county,
                            "major_city": location.major_city,
                            "state": location.state,
                            "county": location.county,
                            "zipcode": location.zipcode,
                            "population_served":location.population_served,
                            "score": 0,
                            "facilities": facilities
                        })
                    else:
                        response["locations"].append({
                            "fips_state_id": location.fips_state,
                            "fips_county_id": location.fips_county,
                            "major_city": location.major_city,
                            "state": location.state,
                            "county": location.county,
                            "zipcode": location.zipcode,
                            "population_served":location.population_served,
                            "score": round(float(data.score), 2),
                            "facilities": facilities
                        })

                response["meta"]["locations"] = len(response["locations"])

            response["meta"]["facilities"] = total_facilities
        # filter for news
        if 'news' in sources or not len(sources):
            queryset = news_models.location.objects.all()
            if request.query_params.get('fips_state'):
                queryset.filter( fips_state = request.query_params.get('fips_state') )

            if request.query_params.get('fips_county'):
                queryset.filter( fips_state = request.query_params.get('fips_county') )

            if request.query_params.get('status'):
                queryset.filter( status = str2bool(request.query_params.get('status')) )

            response["meta"]["cities"] = queryset.count()
            for news in queryset:
                response["cities"].append({
                    "fips_state_id": news.fips_state,
                    "fips_county_id": news.fips_county,
                    "zipcode": news.zipcode,
                    "name": news.city,
                    "county": news.county,
                    "status":news.status,
                    "long": news.position.x if news.position else '',
                    "lat": news.position.y if news.position else '',
                })

        # filter for utilities
        if 'utilities' in sources or not len(sources):

            queryset = Q()
            if request.query_params.get('violation'):
                queryset &= Q( violation = str2bool(request.query_params.get('violation')) )

            response["meta"]["utilities"] = news_models.utility.objects.filter(queryset).count()
            for utility in  news_models.utility.objects.filter(queryset):

                counties_served = []
                for county in news_models.county_served.objects.filter( utility = utility):
                    counties_served.append({
                        "fips_state_id": county.location.fips_state,
                        "fips_county_id": county.location.fips_county,
                        "name": county.location.name
                    })

                response["utilities"].append({
                    "name": utility.name,
                    "has_contaminats": utility.has_contaminats,
                    "url": utility.link,
                    "long": utility.position.x if utility.position else '',
                    "lat":  utility.position.y if utility.position else '',
                    "violation": utility.violation,
                    "violation_points": utility.voilation_points,
                    "people_served": utility.people_served,
                    "counties_served":counties_served
                })


        return Response(response)
