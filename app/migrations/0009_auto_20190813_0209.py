# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-08-13 02:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_location_population_served'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='population',
        ),
        migrations.RemoveField(
            model_name='location',
            name='population_density',
        ),
    ]