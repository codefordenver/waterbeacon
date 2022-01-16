from app import models as app_models
from django.utils import timezone

class Command(BaseCommand):
    def handle(self, *args, **options):
        now = timezone.now()
        year = now.year
        if now.month >= 11:
            quarter = 'q4'
        elif now.month >= 8:
            quarter = 'q3'
        elif now.month >= 5:
            quarter = 'q2'
        else:
            quarter = 'q1'

        # save data rank
        prior_score = 0
        rank = 1
        for  data in app_models.data.objects.filter(quarter = quarter, year = year).order_by('score'):
            if data.score == prior_score:
                data.rank = rank
            else:
                rank += 1
                data.rank = rank
                prior_score = data.score
            data.save()
