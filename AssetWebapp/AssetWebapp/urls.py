from django.conf.urls import patterns, include, url
from django.contrib import admin

from AssetWebapp import settings
from myapp.views import Home, \
 User, Error, Group, Reason, IncrementAsset, DecrementAsset\
, FunctionList, VerifyAsset, RevaluateAsset, Report, ViewAsset


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^home/$', Home.index),
    
    url(r'^$', Home.index),
    
    url(r'^admin/', include(admin.site.urls)),
#     url(r'^accounts/', include(registration.backends.default.urls)),
    url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'change-password.html'}, name='password_change'),
    url(r'^password/change/done/$',
                    'django.contrib.auth.views.password_change', {'template_name': 'change-password-done.html'},
                    name='password_change_done'),
    url(r'^password/reset/$',
                    'django.contrib.auth.views.password_reset',
                    name='password_reset'),
    url(r'^password/reset/done/$',
                  'django.contrib.auth.views.password_reset_done',
                  name='password_reset_done'),
    url(r'^password/reset/complete/$',
                  'django.contrib.auth.views.password_reset_complete',
                  name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                  'django.contrib.auth.views.password_reset_confirm',
                  name='password_reset_confirm'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'login'}),
    # Function List
    url(r'^function-list$', FunctionList.index, name='function-list'),
    # increment asset
    url(r'^increment-asset/$', IncrementAsset.index, name='increment-asset'),
    # view Asset
    url(r'^view-asset/$', ViewAsset.index),
    # increment asset
    url(r'^decrement-asset/$', DecrementAsset.index, name='decrement-asset'),
    url(r'^get-list-stock/(?P<dept_id>\w+)/$', DecrementAsset.getListStock, name='get-list-stock'),
    url(r'^get-list-serial/(?P<stock_id>\w+)/$', DecrementAsset.getListSerial, name='get-list-serial'),
    # verify asset
    url(r'^verify-asset/$', VerifyAsset.index),
    url(r'^verify-asset/(?P<serial_id>\w+)/$', VerifyAsset.verify),
    # revaluate asset
    url(r'^revaluate-asset/$', RevaluateAsset.index),
    # User
    url(r'^user/$', User.list_user, name='user'),
    # add user 
    url(r'^user/add/$', User.add_user, name='delete-user'),
    # delete user 
    url(r'^user/delete/(?P<user_id>\w+)/$', User.delete_user, name='add-user'),
    url(r'^user/(?P<user_id>\w+)/$', User.change_user, name='change-user'),
    url(r'^change-password/$', User.change_password, name='change-password'),
    # Group
    url(r'^group/$', Group.view_group, name='user'),
    url(r'^group/add/$', Group.add_group, name='add-group'),
    url(r'^group/delete/(?P<group_id>\w+)/$', Group.delete_group, name='delete-group'),
    url(r'^group/(?P<group_id>\w+)/$', Group.change_group, name='change-group'),
    # Reason
    url(r'^reason$', Reason.view_reason , name='reason'),
    url(r'^reason/add/$', Reason.add_reason, name='add-reason'),
    url(r'^reason/delete/(?P<reason_id>\w+)/$', Reason.delete_reason, name='delete-reason'),
    url(r'^reason/(?P<reason_id>\w+)/$', Reason.change_reason, name='change-reason'),
    # Report
    url(r'^report/asset-inventory-report$', Report.view_Asset_Inventory_report , name='asset-inventory-report'),
    url(r'^report/verify-asset-report$', Report.verify_asset_report , name='verify-asset-report'),
    # Error page
    url(r'^permission-error/$', Error.permission_error, name='permission-error'),
    url(r'^notfound-error/$', Error.notfound_error, name='notfound-error'),
    # Static directory
    url(regex=r'^report/(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.REPORT_ROOT, 'show_indexes' : True, }),
    url(regex=r'^(?P<path>.*)$', view='django.views.static.serve', kwargs={'document_root': settings.STATIC_ROOT, 'show_indexes' : False, }),
)
