from rest_framework import serializers
from app import models
from api.v1 import mixins


class NodeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.data
