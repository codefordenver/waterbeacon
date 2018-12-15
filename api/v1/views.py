from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q
from django.db.models import Count
from django.http import Http404

from annoying.functions import get_object_or_None
from datetime import datetime, timedelta

from app import models
from api.v1 import ( serializers )


class nodeData(APIView):

    def get(self, request):
        return Response({})

    def post(self, request, format = None):
        return Response(serializer.data, status=status.HTTP_201_CREATED)
