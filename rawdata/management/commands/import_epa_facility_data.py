from rawdata.models import EpaSystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import json
import sys
import os
from datetime import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        #TODO all of this... so ignore for now
        # TODO make this a setting not property in EpaDataGetter class 
        jsonDirectory = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'Facilities')
        processed_rows = 0

        for filename in os.listdir(jsonDirectory):
            with open(os.path.join(jsonDirectory, filename)) as f:
                data = json.loads(f.read())

            for system in data["Results"]["WaterSystems"]:
                if system['PWSActivityCode'] != 'A':
                    continue # we only want active sites so skip others
                try:
                    processed_rows += 1 
                    self.add_watersystem_to_db(system)
                    if (processed_rows % 10000 == 0):
                        self.stdout.write('Processed row %s...' %processed_rows)
                except utils.IntegrityError:
                    self.stdout.write('%s already in the db' % system["PWSId"])
                except:
                    self.stdout.write(system)
                    raise


    def add_watersystem_to_db(self, system):
        # TODO use object.get_or_add? need to make sure this doesn't duplicate each time
        # just truncate the table and reimport? or maybe EpaSystem.objects.all().delete() if FK matters
        obj = EpaSystem(
            FacDerivedStctyFIPS
            SDWAFormalActionCount
            FacDateLastPenalty
            SDWISFlag
            FacState
            FacDerivedHuc
            FacTotalPenalties
            SDWAInspections5yr
            SDWAIDs
            FacLastPenaltyAmt
            FacName
            FacZip
            FacEPARegion
            FacDerivedZip
            NC
            FacFormalActionCount
            ViolFlag
            FacReferencePoint
            FacCity
            FacImpWaterFlg
            FacPenaltyCount
            FacFIPSCode
            SDWA3yrComplQtrsHistory
            FacDerivedWBD
            FacLat
            FacCollectionMethod
            CurrVioFlag
            FacStdCountyName
            SDWAInformalCount
            RegistryID
            FacStreet
            FacAccuracyMeters
            FacCounty
            FacLong
        )
        obj.save()


def format_date(date_string):
    '''convert the dd/mm/yyyy format into a datetime object'''
    if date_string:
        return datetime.strptime(date_string, '%m/%d/%Y')
    return None
