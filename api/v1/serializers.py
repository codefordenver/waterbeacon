from rest_framework import serializers
from subscribe import models as subscribe_models
from app import models as app_models

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_models.location
        fields = ('major_city','county', 'state', 'zipcode', 'neighborhood', 'notes', 'population_served')

class SubscribeSerializer(serializers.ModelSerializer):
    email =  serializers.SerializerMethodField()
    locations = LocationSerializer( many = Ture, read_only = True)
    zipcode = serializers.CharField(required = False, write_only = True)

    class Meta:
        model = subscribe_models.Subscribe
        fields = ('is_active', 'email', 'locations', 'notifications', 'workshop', 'created')

    def get_email(self, instance):
        if instance.user:
            return instance.user.email
        return ''

    def create(self, validated_data):
        pass
