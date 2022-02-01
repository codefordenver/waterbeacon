from rest_framework import serializers
from subscribe import models as subscribe_models
from app import models as app_models
from news import models as news_models
from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_models.location
        fields = ('major_city','county', 'state', 'zipcode', 'neighborhood', 'notes', 'population_served')

class SubscribeSerializer(serializers.ModelSerializer):
    email =  serializers.CharField(required = False)
    locations = LocationSerializer( many = True, read_only = True)
    zipcode = serializers.CharField(required = False, write_only = True, allow_blank=True)

    class Meta:
        model = subscribe_models.Subscribe
        fields = ('is_active', 'zipcode', 'email', 'newsletter', 'locations', 'notifications', 'workshop', 'created')

    def create(self, validated_data):
        user, created =  get_user_model().objects.get_or_create( email = validated_data.get('email').lower(), username = validated_data.get('email').lower())
        subscribe, created = subscribe_models.Subscribe.objects.get_or_create( user = user )
        subscribe.newsletter = validated_data.get('newsletter', False)
        subscribe.workshop = validated_data.get('workshop', False)

        subscribe.save()

        location = get_object_or_None(app_models.location, zipcode = validated_data.get('zipcode', None))
        if location:
            subscribe.locations.add(location  )


        return subscribe


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = news_models.location
        fields =('city', 'county', 'state', 'zipcode')

class AlertSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = news_models.alert
        fields = ('id', 'location' , 'source', 'text', 'published', 'status')
