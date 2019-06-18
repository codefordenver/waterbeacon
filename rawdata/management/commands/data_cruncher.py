import os
from django.conf import settings
from django.core.management.base import BaseCommand
from utils.epa.sdw_data_cruncher import ( SDW_Data_Cruncher )

class Command(BaseCommand):
    def handle(self, *args, **options):
        cruncher = SDW_Data_Cruncher()
        cruncher.calc_state_scores('MI', print_test = True)
