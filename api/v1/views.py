from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Count
from django.http import Http404

from annoying.functions import get_object_or_None
from datetime import datetime, timedelta

from app import models as app_models
from news import models as news_models

from api.v1 import ( serializers )
from utils.utils import ( str2bool )


class nodeData(APIView):
    # /v1/data/?status=true&violation=true


    def get(self, request):
        response = {"meta":{"sensors": 0, "cities": 0, "utilities": 0},"cities":[], "sensors":[],"utilities" :[]}

        sources = request.query_params.get('sources','').split(',')

        # filter for sensor
        if 'sensors' in sources or not len(sources):
            queryset = app_models.node.objects.all()
            if request.query_params.get('status'):
                queryset.filter( status = str2bool(request.query_params.get('status')) )
            for sensor in queryset:
                data = models.data.objects.filter(node = sensor).latest('timestamp')
                response["sensors"].append({
                    "fips_state_id": sensor.fips_state,
                    "fips_county_id": sensor.fips_county,
                    "name": sensor.name,
                    "state": sensor.state,
                    "county": sensor.county,
                    "long": sensor.position.x if sensor.position else '',
                    "lat":sensor.position.y if sensor.position else '',
                    "score": sensor.score,
                    "status": sensor.stauts,
                    "disolved_oxygen": sensor.meta.get('disolved_oxygen',0),
                    "ph": sensor.meta.get('ph',0),
                    "temperature_change": sensor.meta.get('temperature_change',0),
                    "turbidity": sensor.meta.get('turbidity',0),
                })

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
            queryset = news_models.utility.objects.all()

            if request.query_params.get('violation'):
                queryset.filter( violation = str2bool(request.query_params.get('violation')) )

            response["meta"]["utilities"] = queryset.count()
            for utility in queryset:

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


        return Response()

    def post(self, request, format = None):
        return Response(serializer.data, status=status.HTTP_201_CREATED)
