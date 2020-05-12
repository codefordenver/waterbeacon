import os
from django.core.management.base import BaseCommand
from news import tasks

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--skip_locations',
            action='store_true',
            dest='skip_locations',
            default=True,
            help='Skip Searching Specific Locations')

    def handle(self, *args, **options):

        tasks.TweetWaterAdvisoryReader(
            consumer_key =  os.getenv('TWITTER_CONSUMER_KEY'),
            consumer_secret =  os.getenv('TWITTER_CONSUMER_SECRET'),
            access_token =  os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret =  os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            skip_locations = options['skip_locations']
        )
