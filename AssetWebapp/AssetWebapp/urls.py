from django.conf.urls import patterns, include, url
from django.contrib import admin

from AssetWebapp import settings

admin.autodiscover()

urlpatterns = patterns('',
	#AdminManagement
    url(r'^admin/', include('AdminManagement.urls')),
    #AssetManagement
    url(r'^', include('myapp.urls')),
    # Static directory
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)