from django.conf.urls import patterns, include, url
from django.contrib import admin

from eAlarm import settings
from myapp.views import Home, DeviceProperties, AddDeviceProperties, EditDeviceProperties, Area, AddArea, DeviceInfor, EditArea\
, Device, User, Error, Group,ListDevice,AddDevice


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home$', Home.index),
    url(r'^device-infor$', DeviceInfor.index),
    url(r'^$', Home.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^change-password$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name='login'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'login'}),
    url(r'^device-property$', DeviceProperties.index),
    url(r'^add-device-property$', AddDeviceProperties.index,name='add-device-property'),
    url(r'^edit-device-property$', EditDeviceProperties.index,name='add-device-property'),
	url(r'^area$', Area.index),
    url(r'^add-area$', AddArea.index),
    url(r'^add-area$', AddArea.index,name='add-area'),
    url(r'^edit-area$', EditArea.index),
    url(r'^device$', Device.index),
    url(r'^device-list$', ListDevice.index),
    url(r'^add-device', AddDevice.index),
    url(r'^add-device', AddDevice.index,name='add-device'),
    
    # User
    url(r'^user$', User.view_user,name='user'),
    url(r'^user/add/$', User.add_user,name='delete-user'),
    url(r'^user/delete/(?P<user_id>\w+)/$', User.delete_user,name='add-user'),
    url(r'^user/(?P<user_id>\w+)/$', User.change_user,name='change-user'),
    # Group
    url(r'^group$', Group.view_group,name='user'),
    url(r'^group/add/$', Group.add_group,name='add-group'),
    url(r'^group/delete/(?P<group_id>\w+)/$', Group.delete_group,name='delete-group'),
    url(r'^group/(?P<group_id>\w+)/$', Group.change_group,name='change-group'),
    
    url(r'^permission-error$', Error.permission_error,name='permission-error'),
    url(r'^notfound-error$', Error.notfound_error,name='notfound-error'),
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)
