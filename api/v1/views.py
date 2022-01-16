from django.db.models.expressions import Value
from django.db.models.fields import BooleanField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import F, Q


from . import serializers
from app import models as app_models
from subscribe import models as subscribe_models
from news import models as news_models
from rawdata import models as raw_models
from utils.utils import str2bool
from django_pandas.io import read_frame
from django.db.models import Max, Min, Avg
import math


class locationData(APIView):
    def _get_quarter_list(self, quarters):
        num_left = 8 - quarters.count()
        initial_values = list(quarters.order_by("-year", "-quarter")[:8])
        if num_left <= 0:
            return initial_values

        min_year = quarters.aggregate(Min("year"))["year__min"]
        quarter_options = ["q1", "q2", "q3", "q4"]
        min_quarter = quarters.filter(year=min_year).aggregate(Min("quarter"))[
            "quarter__min"
        ]
        min_quarter_index = quarter_options.index(min_quarter)

        num_left_index = num_left + 1
        for i in range(1, num_left_index):
            quarter_diff = min_quarter_index - i
            year_diff = math.floor(quarter_diff / 4)
            quarter_diff = quarter_diff - year_diff * 4
            quarter = quarter_options[quarter_diff]
            year = min_year + year_diff
            initial_values.append({"quarter": quarter, "year": year, "existing": False})
        return initial_values

    # /v1/data/?sources=locations
    def get(self, request):
        response = {
            "meta": {"cities": 0, "utilities": 0, "locations": 0},
            "locations": [],
            "utilities": [],
            "cities": [],
            "states": [],
            "quarters": [],
            "top_locations": [],
        }
        quarters = (
            app_models.data.objects.values("quarter", "year")
            .annotate(existing=Value(True, output_field=BooleanField()))
            .distinct()
        )
        max_year = quarters.aggregate(Max("year"))["year__max"]
        max_quarter = quarters.filter(year=max_year).aggregate(Max("quarter"))[
            "quarter__max"
        ]

        response["quarters"] = self._get_quarter_list(quarters)

        # insert filter for quarter and year
        queryset = Q()
        has_specified_period = request.query_params.get(
            "quarter"
        ) and request.query_params.get("year")

        if has_specified_period:
            queryset &= Q(quarter=request.query_params.get("quarter"))
            queryset &= Q(year=request.query_params.get("year"))
        else:
            queryset &= Q(year=max_year)
            queryset &= Q(quarter=max_quarter)

        # filter for locations
        sources = request.query_params.get("sources", "").split(",")
        if "locations" in sources or not len(sources):
            data = app_models.data.objects.filter(
                queryset, location__major_city__isnull=False
            ).values(
                "rank",
                "score",
                fipsState=F("location__fips_state"),
                fipsCounty=F("location__fips_county"),
                majorCity=F("location__major_city"),
                state=F("location__state"),
                county=F("location__county"),
                zipCode=F("location__zipcode"),
                populationServed=F("location__population_served"),
            )
            response["locations"] = data
            response["top_locations"] = data.order_by("-score")[0:3]
            response["meta"]["locations"] = len(data)
            response["states"] = data.values("fipsState").annotate(
                avg=Avg("score"), max=Max("score"), min=Min("score")
            )

        # filter for news
        if "news" in sources or not len(sources):
            queryset = news_models.location.objects.all()
            if request.query_params.get("fips_state"):
                queryset.filter(fips_state=request.query_params.get("fips_state"))

            if request.query_params.get("fips_county"):
                queryset.filter(fips_state=request.query_params.get("fips_county"))

            if request.query_params.get("status"):
                queryset.filter(status=str2bool(request.query_params.get("status")))

            response["meta"]["cities"] = queryset.count()
            for news in queryset:
                response["cities"].append(
                    {
                        "fips_state_id": news.fips_state,
                        "fips_county_id": news.fips_county,
                        "zipcode": news.zipcode,
                        "name": news.city,
                        "county": news.county,
                        "status": news.status,
                        "long": news.position.x if news.position else "",
                        "lat": news.position.y if news.position else "",
                    }
                )

        # TODO: Finish doing utilities, add query param
        # filter for utilities
        if "utilities" in sources or not len(sources):
            # maybe there is a better way to merge these two records than using pandas?
            facility_rd = (
                raw_models.EpaFacilitySystem.objects.filter(FacLat__isnull=False)
                .filter(FacLong__isnull=False)
                .filter(PWSId__isnull=False)
                .filter(FacFIPSCode__isnull=False)
                .filter(SDWASystemTypes="Community water system")
                .values(
                    fipsCode=F("FacFIPSCode"),
                    lat=F("FacLat"),
                    long=F("FacLong"),
                    pwsId=F("PWSId"),
                    registryId=F("RegistryID"),
                )
            )
            facility_df = read_frame(facility_rd)

            watersystem_rd = (
                raw_models.EpaWaterSystem.objects.filter(PWSId__isnull=False)
                .filter(PWSTypeCode="CWS")
                .filter(Vioremain__gte=1)
                .values(
                    pwsId=F("PWSId"),
                    facName=F("PWSName"),
                )
            )
            watersystem_df = read_frame(watersystem_rd)

            df = watersystem_df.merge(facility_df, how="left").dropna()

            utilities = df.to_dict("records")
            response["meta"]["utilities"] = len(utilities)

            response["utilities"] = utilities

        return Response(response)


class SubscribeView(generics.CreateAPIView):
    queryset = subscribe_models.Subscribe.objects.all()
    serializer_class = serializers.SubscribeSerializer
