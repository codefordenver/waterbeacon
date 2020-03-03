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
from utils.utils import (str2bool)
import math


class locationData(APIView):
    # /v1/data/?sources=locations

    # TODO
    # this does way too much work. ideally, there would be a process to
    #   collect, sanitize, analyze, store the data in the right format
    #   (maybe with checkpoints so it can stop/start)
    # given current structure with too many commands, we should move more logic into the data cruncher and
    # simply select it here

    def get(self, request):
        response = {"meta": {"cities": 0, "utilities": 0, "locations": 0, "facilities": 0},
                    "locations": [], "utilities": [], 'cities': [], 'facilities': []}

        sources = request.query_params.get('sources', '').split(',')

        # filter for locations
        if 'locations' in sources or not len(sources):

            # okay, wtf? how do i include the the data.score column here?
            # queryset = app_models.location.objects.filter(data__score__gt=0)

            queryset = app_models.Location.objects.raw(
                r'select l.id, l.fips_state, l.fips_county, l.major_city, l.state, l.county, l.zipcode, l.population_served, d.score from "app_location" l join "app_data" d on d.location_id = l.id where d.score > 0')

            facilities_rd = raw_models.EpaFacilitySystem.objects.filter(
                CurrVioFlag=1).values('FacFIPSCode', 'PWSId', 'FacName', 'FacLong', 'FacLat')
            fac_df = read_frame(facilities_rd)
            fac_df.rename(columns={'FacLong': 'long',
                                   'FacLat': 'lat'}, inplace=True)
            total_facilities = 0

            for location in queryset:
                facilities = fac_df[fac_df['FacFIPSCode'] ==
                                    location.fips_county].to_dict('records')
                if math.isnan(location.score):
                    score = 0
                else:
                    score = round(float(location.score), 2)

                response["locations"].append({
                    "fips_state_id": location.fips_state,
                    "fips_county_id": location.fips_county,
                    "major_city": location.major_city,
                    "state": location.state,
                    "county": location.county,
                    "zipcode": location.zipcode,
                    "population_served": location.population_served,
                    "score": score,
                    "facilities": facilities})

            response["meta"]["locations"] = queryset.count()
            response["meta"]["facilities"] = total_facilities

        # filter for news
        if 'news' in sources or not len(sources):
            queryset = news_models.location.objects.all()
            if request.query_params.get('fips_state'):
                queryset.filter(
                    fips_state=request.query_params.get('fips_state'))

            if request.query_params.get('fips_county'):
                queryset.filter(
                    fips_state=request.query_params.get('fips_county'))

            if request.query_params.get('status'):
                queryset.filter(status=str2bool(
                    request.query_params.get('status')))

            response["meta"]["cities"] = queryset.count()
            for news in queryset:
                response["cities"].append({
                    "fips_state_id": news.fips_state,
                    "fips_county_id": news.fips_county,
                    "zipcode": news.zipcode,
                    "name": news.city,
                    "county": news.county,
                    "status": news.status,
                    "long": news.position.x if news.position else '',
                    "lat": news.position.y if news.position else '',
                })

        # filter for utilities
        if 'utilities' in sources or not len(sources):

            queryset = Q()
            if request.query_params.get('violation'):
                queryset &= Q(violation=str2bool(
                    request.query_params.get('violation')))

            response["meta"]["utilities"] = news_models.utility.objects.filter(
                queryset).count()
            for utility in news_models.utility.objects.filter(queryset):

                counties_served = []
                for county in news_models.county_served.objects.filter(utility=utility):
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
                    "counties_served": counties_served
                })

        return Response(response)
