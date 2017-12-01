from django.conf.urls import url, include
from rest_framework import routers
import views

urlpatterns = [
	url(r'^data/$', views.NodeListView.as_view()),
	url(r'^news/$',views.NewsListView.as_view()),
]
