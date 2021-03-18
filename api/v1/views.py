from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F, Q


from app import models as app_models
from news import models as news_models
from rawdata import models as raw_models
from utils.utils import str2bool


class locationData(APIView):
    # /v1/data/?sources=locations

    def get(self, request):
        response = {
            "meta": {"cities": 0, "utilities": 0, "locations": 0},
            "locations": [],
            "utilities": [],
            "cities": [],
        }

        sources = request.query_params.get("sources", "").split(",")

        # filter for locations
        if "locations" in sources or not len(sources):
            data = app_models.data.objects.filter(
                location__major_city__isnull=False
            ).values(
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
            response["meta"]["locations"] = len(data)

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
            print(sources)
            utilities_rd = (
                raw_models.EpaFacilitySystem.objects.filter(Score__gt=0)
                .filter(SDWASystemTypes="Community water system")
                .values(
                    fipsCode=F("FacFIPSCode"),
                    lat=F("FacLat"),
                    long=F("FacLong"),
                    pwsId=F("PWSId"),
                    registryId=F("RegistryID"),
                    score=F("Score"),
                )
            )

            response["meta"]["utilities"] = len(utilities_rd)

            response["utilities"].append(utilities_rd)

            # queryset = Q()
            # if request.query_params.get("violation"):
            #     queryset &= Q(violation=str2bool(request.query_params.get("violation")))

            # response["meta"]["utilities"] = news_models.utility.objects.filter(
            #     queryset
            # ).count()
            # for utility in news_models.utility.objects.filter(queryset):

            #     counties_served = []
            #     for county in news_models.county_served.objects.filter(utility=utility):
            #         counties_served.append(
            #             {
            #                 "fips_state_id": county.location.fips_state,
            #                 "fips_county_id": county.location.fips_county,
            #                 "name": county.location.name,
            #             }
            #         )

            #     response["utilities"].append(
            #         {
            #             "name": utility.name,
            #             "has_contaminats": utility.has_contaminats,
            #             "url": utility.link,
            #             "long": utility.position.x if utility.position else "",
            #             "lat": utility.position.y if utility.position else "",
            #             "violation": utility.violation,
            #             "violation_points": utility.voilation_points,
            #             "people_served": utility.people_served,
            #             "counties_served": counties_served,
            #         }
            #     )

        return Response(response)
