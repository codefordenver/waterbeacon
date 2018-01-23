from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.utils import int_or_none

def add_envelope(request, data, meta={}):
    env = {}
    env['data'] = data
    env['meta'] = meta
    env['meta']['request'] = request.build_absolute_uri(request.get_full_path())
    return env

class BaseView( APIView):
    def __init__(self, *args, **kwargs):
        self.rows_found = None
        super(BaseView, self).__init__(*args, **kwargs)

    def get(self, request, pk=None, format=None):
        queryset = self._get_queryset(request, pk)
        srlzr = self._get_serializer_class()
        serializer = srlzr(queryset, many=self.many, context={'request': request})
        return self._send_response(serializer.data)

    def _send_response(self, data, meta=None):
        return Response(data)

    def _get_meta_serializer_function(self): return lambda request, queryset: {}

    def _get_model(self): pass
    def _get_queryset(self, request, pk): pass
    def _get_serializer_class(self): pass


class StandardListView(BaseView):
    many = True
    def _get_queryset(self, request, pk=None):
        limit = None
        if 'limit' in request.query_params:
            val = int_or_none(request.query_params['limit'])
            if val is not None and val >= 0:
                limit = val
        offset = 0
        if 'offset' in request.query_params:
            val = int_or_none(request.query_params['offset'])
            if val is not None and val >= 0:
                offset = val
        model = self._get_model()
        queryset = model.objects.all()
        self.rows_found = queryset.count()
        if limit:
            queryset = queryset[offset:offset + limit]
        return queryset


class StandardDetailView(BaseView):
    many = False
    def _get_queryset(self, request, pk):
        model = self._get_model()
        queryset = model.objects.get(pk=pk)
        return queryset


class SerializeFunctionDetailView(BaseView):
    many = False
    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(self._get_model(), pk=pk)
        srlzr = self._get_serializer_function()
        data = srlzr(obj, request)
        return self._send_response(data)


class SerializeFunctionListView(BaseView):
    many = True
    def get(self, request):
        limit = None
        if 'limit' in request.query_params:
            val = int_or_none(request.query_params['limit'])
            if val is not None and val >= 0:
                limit = val
        offset = 0
        if 'offset' in request.query_params:
            val = int_or_none(request.query_params['offset'])
            if val is not None and val >= 0:
                offset = val
        srlzr = self._get_serializer_function()
        meta_srlzr = self._get_meta_serializer_function()
        queryset = self._get_queryset()
        queryset = self._filter_queryset(request, queryset)
        queryset = self._sort_queryset(request, queryset)
        self.rows_found = queryset.count()
        if limit:
            queryset = queryset[offset:offset + limit]
        data = srlzr(queryset, request)
        meta = meta_srlzr(queryset, request)
        return self._send_response(data, meta)

    def _get_queryset(self):
        model = self._get_model()
        queryset = model.objects.all()
        return queryset

    def _filter_queryset(self, request, queryset):
        return queryset

    def _sort_queryset(self, request, queryset):
        return queryset


class EnvelopeView(BaseView):
    meta = {}

    def _send_response(self, data, meta=None):
        if meta is None:
            meta = {}
        self.meta.update(meta)
        self.meta['rows_found'] = self.rows_found
        self.meta['rows_sent'] = len(data)
        return Response(add_envelope(self.request, data, self.meta))
