from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from myapp.views import Home



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'AssetWebapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home$', Home.index, name='home'),
    url(r'^test$', Home.test, name='test'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'myapp.views.Home.signin', name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'login'}),
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)
