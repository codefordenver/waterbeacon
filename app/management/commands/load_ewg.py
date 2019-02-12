import os
from django.core.management.base import BaseCommand
from news import tasks


class Command(BaseCommand):

    def handle(self, *args, **options):
        tasks.EWG_TapwaterReader()
