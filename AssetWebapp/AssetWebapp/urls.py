from django.conf.urls import patterns, include, url
from django.contrib import admin

from AssetWebapp import settings

admin.autodiscover()

urlpatterns = patterns('',
	#AdminManagement
    url(r'^', include('AdminManagement.urls')),
    #AssetManagement
    url(r'^', include('myapp.urls')),
    url(r'^permission-error/$', 'myapp.views.Error.permission_error', name='permission-error'),
    url(r'^notfound-error/$', 'myapp.views.Error.notfound_error', name='notfound-error'),
    url(r'^error-page/$', 'myapp.views.Error.error', name='error-page'),
    # Static directory
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)