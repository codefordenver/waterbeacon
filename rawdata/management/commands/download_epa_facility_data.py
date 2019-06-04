import os
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_downloader import ( SDW_Downloader )

class Command(BaseCommand):
    def handle(self, *args, **options):

        target_dir = os.path.join(
            settings.BASE_DIR, settings.EPA_DATA_DIRECTORY)


        downloader = SDW_Downloader()
        downloader.get_facility_data(target_dir)
