from django.conf.urls import url, include
from django.conf.urls import url
from api.v1 import views

urlpatterns = [
    url(r'^data/', views.nodeData.as_view(), name='node-data'),
]
