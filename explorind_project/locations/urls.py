from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import location
	
urlpatterns = patterns('',
	
	url(r'^(?P<locationname>[A-Za-z]+)/$', location, name='location'),
	url(r'^(?P<locationname>[A-Za-z]+)/(?P<placeofinterest>[A-Za-z]+)/$', location, name = 'placeofinterest'),
	
	)