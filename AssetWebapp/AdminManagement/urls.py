from django.conf.urls import patterns, url

from AdminManagement.views import User, Group


urlpatterns = patterns('',
	url(r'^password/change/$', 'django.contrib.auth.views.password_change', {'template_name': 'admin/user/change-password.html'}, name='password_change'),
	url(r'^password/change/done/$',
			'django.contrib.auth.views.password_change', {'template_name': 'admin/user/change-password-done.html'},
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
	# User
	url(r'^user/$', User.list_user, name='user'),
	url(r'^user/add/$', User.add_user, name='delete-user'),
	url(r'^user/delete/(?P<user_id>\w+)/$', User.delete_user, name='add-user'),
	url(r'^user/(?P<user_id>\w+)/$', User.change_user, name='change-user'),
	# Group
	url(r'^group/$', Group.view_group, name='user'),
	url(r'^group/add/$', Group.add_group, name='add-group'),
	url(r'^group/delete/(?P<group_id>\w+)/$', Group.delete_group, name='delete-group'),
	url(r'^group/(?P<group_id>\w+)/$', Group.change_group, name='change-group'),
	#login
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/signin.html'}, name='login'),
	#logout
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'login'}),
)