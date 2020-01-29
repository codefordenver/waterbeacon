from rawdata.models import EpaWaterSystem
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import utils
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from utils.epa.sdw_importer import ( SDW_Importer )

class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        # TODO make this a setting not property in EpaDataGetter class WATER_TYPE = 'WaterSystems'
        jsonDirectory = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY, 'WaterSystems')
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
                    if system[columns.index('PWSActivityCode')] != 'A':
                        continue # we only want active sites so skip others
                    try:
                        processed_rows += 1
                        importer.add_watersystem_to_db(system, columns)
                        if (processed_rows % 10000 == 0):
                            self.stdout.write('Processed row %s...' %processed_rows)
                    except utils.IntegrityError:
                        self.stdout.write('%s already in the db' % system[columns.index("PWSId")])
                    except:
                        self.stdout.write('%s' %system)
                        raise