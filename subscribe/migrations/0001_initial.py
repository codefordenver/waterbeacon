# Generated by Django 3.0.12 on 2021-11-23 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auto_20211123_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('workshop', models.BooleanField(default=True)),
                ('newsletter', models.BooleanField(default=True)),
                ('notifications', models.BooleanField(default=True)),
                ('mailchimp_member_id', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('locations', models.ManyToManyField(to='app.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
