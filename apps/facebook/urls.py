from django.conf.urls import url
from . import views



urlpatterns=[
	url(r'^$', views.index),
	url(r'^new$', views.new),
	url(r'^login$', views.login),
	url(r'^friends/$', views.friends),
	url(r'logout/$', views.logout),
	url(r'poke/(?P<id>\d+)$', views.poke)
	
]