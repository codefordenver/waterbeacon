from django.conf.urls import url, include
from django.conf.urls import url
from api.v1 import views

urlpatterns = [
    url(r'^data/', views.locationData.as_view(), name='location-data'),
    #url(r'^subscribe/', views.subscribe.as_view(), name='subscribe'),
]
