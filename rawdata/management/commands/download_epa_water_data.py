import os
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.epa_sdw_downloader import ( EPA_SDW_Downloader )

class Command(BaseCommand):
    def handle(self, *args, **options):
        target_dir = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY)


        downloader = EPA_SDW_Downloader()
        downloader.get_water_data(target_dir)
