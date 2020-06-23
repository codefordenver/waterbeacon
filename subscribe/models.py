from django.db import models
from django.conf import settings
from app import models as app_models

# Create your models here.
class subscribe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.PROTECT)
    locations = models.ManyToManyField(app_models.location)
