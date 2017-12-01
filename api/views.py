from api import serializers
from api import base_views
from app import models as app_models
from news import models as news_models

class NodeListView(base_views.SerializeFunctionListView):
    def _get_model(self):
        return app_models.node

    def _get_serializer_function(self):
        return serializers.NodeSerializer

    def _filter_queryset(self, request, queryset):

    	# long / lat  filter
    	if request.query_params.get('loc_start') and request.query_params.get('loc_end'):
    		pass

    	# tags filter
    	if request.query_params.get('tags'):
    		pass

    	# device name
    	if request.query_params.get('name'):
    		pass

    	# time filter
    	if request.query_params.get('date_st'):
    		pass

    	if request.query_params.get('end_st'):
    		pass

    	return queryset

class NewsListView(base_views.SerializeFunctionListView):
    def _get_model(self):
        return news_models.node

    def _get_serializer_function(self):
        return serializers.NewsSerializer

    def _filter_queryset(self, request, queryset):

    	if request.query_params.get('city'):
    		pass

    	if request.query_params.get('zipcode'):
    		pass

    	if request.query_params.get('limit'):
    		pass

    	if request.query_params.get('days_ago'):
    		pass

    	return queryset
