from rawdata.models import EpaFacilitySystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import (SDW_Importer)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class FACILITY_TYPE = 'Facilities'
        jsonDirectory = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'Facilities')
        processed_rows = 0

        importer = SDW_Importer()
        for filename in os.listdir(jsonDirectory):
            with open(os.path.join(jsonDirectory, filename)) as f:
                data = csv.reader(f)

                columns = []
                line_cnt = -1
                for system in data:
                    line_cnt += 1
                    if line_cnt == 0:
                        columns = system
                        continue
                    try:
                        processed_rows += 1
                        if len(system[columns.index("SDWAIDs")]) > 9:
                            # multiple water facilities included
                            full_id_list = system[columns.index(
                                "SDWAIDs")].split(' ')
                            for sdwa_id in full_id_list:
                                system[columns.index("SDWAIDs")] = sdwa_id
                                importer.add_epafacility_to_db(system, columns)
                        else:
                            importer.add_epafacility_to_db(system, columns)
                        if (processed_rows % 10000 == 0):
                            self.stdout.write(
                                'Processed row %s...' % processed_rows)
                    except utils.IntegrityError:
                        self.stdout.write('%s already in the db' %
                                          system[columns.index("RegistryID")])
                    except:
                        self.stdout.write('%s' % system)
                        raise
