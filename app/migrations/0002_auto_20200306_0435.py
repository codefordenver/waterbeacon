# Generated by Django 3.0.2 on 2020-03-06 04:35

from django.db import migrations, models
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='address_key',
        ),
        migrations.AddField(
            model_name='facility',
            name='city',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='county',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='state',
            field=localflavor.us.models.USStateField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='zipcode',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='facility',
            name='facility_type',
            field=models.CharField(choices=[('CWS', 'Community Water System'), ('TNCWS', 'Transient Non-Community Water System'), ('NTNCWS', 'Non-Transient Non-Community Water System'), ('OTHER', 'Other')], max_length=255),
        ),
        migrations.AlterField(
            model_name='facility',
            name='registry_id',
            field=models.CharField(max_length=12),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
