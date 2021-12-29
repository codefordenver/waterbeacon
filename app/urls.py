
from django.conf.urls import url
from . import views

urlpatterns = [
    url('csrf/', views.csrf),
    url(r'^$', views.index),
]
