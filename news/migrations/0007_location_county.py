# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-01 01:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_location_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='county',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
