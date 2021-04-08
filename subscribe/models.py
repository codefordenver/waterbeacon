from django.db import models
from django.conf import settings
from app import models as app_models

# Create your models here.
class Subscribe(models.Model):
    is_active = models.BooleanField(default=True)
    workshop = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.PROTECT)
    locations = models.ManyToManyField(app_models.location)
    notifications = models.BooleanField(default=True)
    mailchimp_member_id = models.CharField(max_length=255, null=True, blank=True,default='')
    created = models.DateTimeField( null=True, auto_now_add=True)
