# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ZipCode(models.Model):
    zip_code = models.CharField(max_length=10)


class Subscribers(models.Model):
    user = models.ForeignKey(User)
    zip_code = models.ManyToManyField(ZipCode)
