from django.core.management.base import BaseCommand
from app import models as app_models
from rawdata import models as raw_models


class Command(BaseCommand):

    def handle(self, *args, **options):

        for location in app_models.location.objects.all():
            location.facilities.clear()
            print "Fips County: %s [%s]" % (location.fips_county, location.state)
            qs = raw_models.EpaFacilitySystem.objects.filter(FacFIPSCode = location.fips_county)
            for facility in qs:
                location.facilities.add(facility)
            print "%s locations added" % ( qs.count())
