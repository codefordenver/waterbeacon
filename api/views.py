from api import serializers
from api import base_views
from app import models

class NodeListView(base_views.SerializeFunctionListView):
    def _get_model(self):
        return models.node

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