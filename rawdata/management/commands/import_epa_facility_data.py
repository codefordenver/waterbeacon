from rawdata.models import EpaFacilitySystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import csv
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import (SDW_Importer)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class FACILITY_TYPE = 'Facilities'
        csv = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'Facilities')
        processed_rows = 0

        importer = SDW_Importer()
        for filename in os.listdir(csv):
            path = (os.path.join(csv, filename))
            try:
                facilities_df = pd.read_csv(path)
            except:
                self.stdout.write('%s data corrupted' % filename)
                continue
            if facilities_df.empty:
                continue
            facilities_df["Score"] = facilities_df["Score"].fillna(0)
            facilities_df["FacDerivedStctyFIPS"] = facilities_df["FacDerivedStctyFIPS"].fillna(0)
            facilities_df["FacDerivedStctyFIPS"] = facilities_df.apply(lambda x: str(x['FacDerivedStctyFIPS']).rstrip('0').rstrip('.').zfill(5), axis = 1)
            facilities_df["FacDerivedZip"] = facilities_df["FacDerivedZip"].fillna(0)
            facilities_df["FacDerivedZip"] = facilities_df.apply(lambda x: str(x['FacDerivedZip']).rstrip('0').rstrip('.').zfill(5), axis = 1)
            facilities_df["FacEPARegion"] = facilities_df["FacEPARegion"].fillna(0)
            facilities_df["FacEPARegion"] = facilities_df.apply(lambda x: str(x['FacEPARegion']).rstrip('0').rstrip('.').zfill(2), axis = 1)
            facilities_df.fillna('', inplace = True)
            line_cnt = 0
            for facility in facilities_df.itertuples():
                line_cnt += 1
                try:
                    processed_rows += 1
                    if len(facility.SDWAIDs) > 9:
                        # multiple water facilities included
                        full_id_list = facility.SDWAIDs.split(' ')
                        for sdwa_id in full_id_list:
                            facility.SDWAIDs = sdwa_id
                            importer.add_epafacility_to_db(facility)
                    else:
                        importer.add_epafacility_to_db(facility)
                    if (processed_rows % 10000 == 0):
                        self.stdout.write(
                            'Processed row %s...' % processed_rows)
                except utils.IntegrityError:
                    self.stdout.write('%s already in the db' %
                                        facility["RegistryID"])
                except:
                    self.stdout.write('%s' % facility.FacState)
                    raise
