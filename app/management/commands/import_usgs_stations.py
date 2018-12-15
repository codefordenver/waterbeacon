import csv
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from app import models
import addfips
from django.contrib.gis.geos import Point
from annoying.functions import get_object_or_None
from utils.log import log
from utils.utils import ( getStateAbbrev )

class Command(BaseCommand):

    def handle(self, *args, **options):
        baseDir  = settings.BASE_DIR
        af = addfips.AddFIPS()

        with open('%s/utils/crawlers/usgs_station/stations.csv' % (baseDir)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for line, row in enumerate(csv_reader):
                if line == 0: # header
                    continue

                site_no, url, lat, long, id, county, state, hydrolic_unit_id, id2 = row
                state_fips = af.get_state_fips(state)
                county_fips = af.get_county_fips(county, state=state)

                node = get_object_or_None(models.node, name = site_no)
                if not node:

                    node = models.node()
                    node.name = site_no
                    node.position = Point( float(lat), float(long))
                    node.county = county
                    node.state = getStateAbbrev(state)
                    node.fips_state = state_fips
                    node.fips_county = county_fips

                    node.meta = json.dumps({'site_no': site_no, 'hydrolic_unit_id':hydrolic_unit_id, 'id2': id2 })
                    node.save()
                    log('node %s - insert' % ( site_no ), 'success')
                else:
                    log('node %s - exists' % ( site_no ), 'info')
