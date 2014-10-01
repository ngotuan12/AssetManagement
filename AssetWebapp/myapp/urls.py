from django.conf.urls import patterns, url

from myapp.views import Home, Department, FunctionList, IncrementAsset, \
	EditIncrementAsset, ViewAsset, UpgradeAsset, DecrementAsset, VerifyAsset, \
	RevaluateAsset, EvaluationAsset, TransferAsset, ListProject, ListSupplier, \
	AssetState, Reason, JoinReleaseAsset, AmortizeAsset, AssetType, Report, Error\
	,Goal,AssetVolatility,ListCountry,App,BarCode,PrintAsset


urlpatterns = patterns('',
    url(r'^home/$', Home.index,name = 'home'),
    url(r'^$', Home.index),
    url(r'^invoice/$', Home.invoice),
    url(r'^tree/$', Home.tree),
    url(r'^invoice/(?P<asset_id>\w+)/$', PrintAsset.print_asset, name='print_asset'),
    # Department
    url(r'^department/$', Department.index, name='department'),
    url(r'^department/add/(?P<parent_id>\w+)/$', Department.add, name='department'),
    url(r'^department/edit/(?P<dept_id>\w+)/$', Department.edit, name='department'),
    url(r'^department/delete/(?P<dept_id>\w+)/$', Department.delete, name='department'),
    #Country
    url(r'^country/$', ListCountry.index, name='country'),
	# App
	url(r'^list-app/$', App.index,name='app'),
	url(r'^app/add/$', App.add_app,name='add-app'),
	url(r'^edit-app/(?P<app_id>\w+)/$', App.edit_app,name='edit-app'),
	url(r'^app/delete/(?P<app_id>\w+)/$', App.delete_app,name='delete-app'),
    # Function List
    url(r'^function-list$', FunctionList.index, name='function-list'),
    # increment asset
    url(r'^increment-asset/$', IncrementAsset.index, name='increment-asset'),
    # edit increment asset
    url(r'^edit-increment-asset/(?P<asset_id>\w+)/$', EditIncrementAsset.index),
    # view Asset
    url(r'^view-asset/$', ViewAsset.index),
    # upgrade asset
    url(r'^upgrade-asset/$', UpgradeAsset.index),
    # increment asset
    url(r'^decrement-asset/$', DecrementAsset.index, name='decrement-asset'),
    url(r'^get-list-stock/(?P<dept_id>\w+)/$', DecrementAsset.getListStock, name='get-list-stock'),
    url(r'^get-list-serial/(?P<stock_id>\w+)/$', DecrementAsset.getListSerial, name='get-list-serial'),
    # verify asset
    url(r'^verify-asset/$', VerifyAsset.index,name='verify-asset'),
    url(r'^verify-asset/(?P<serial_id>\w+)/$', VerifyAsset.verify),
    # revaluate asset
    url(r'^revaluate-asset/$', RevaluateAsset.index),
    # evaluation asset
    url(r'^evaluation-asset/$', EvaluationAsset.index),
    # evaluation asset
    url(r'^transfer-asset/$', TransferAsset.index),
    # list project
    url(r'^list-project/$', ListProject.index,name='list-project'),
    #add project
    url(r'^project/add/$', ListProject.add_project,name='add-project'),
    # edit project
    url(r'^edit-project/(?P<project_id>\w+)/$', ListProject.edit_project,name='edit-project'),
    #delete project
    url(r'^project/delete/(?P<project_id>\w+)/$', ListProject.delete_project,name='delete-project'),
    # list supplier
    url(r'^list-supplier/$', ListSupplier.index,name='supplier'),
    #add supplier
    url(r'^supplier/add/$', ListSupplier.add_supplier,name='add-supplier'),
    # edit supplier
    url(r'^edit-supplier/(?P<supplier_id>\w+)/$', ListSupplier.edit_supplier,name='edit-supplier'),
    #delete supplier
    url(r'^supplier/delete/(?P<supplier_id>\w+)/$', ListSupplier.delete_supplier,name='delete-supplier'),
#     Bar code
	url(r'^bar-code/$', BarCode.barcode,name='bar-code'),
    #AssetState
    url(r'^asset-state/$', AssetState.index,name='asset-state'),
    url(r'^state/add/(?P<parent_id>\w+)/$', AssetState.add, name='add-asset-state'),
    url(r'^state/edit/(?P<state_id>\w+)/$', AssetState.edit, name='edit-asset-state'),
    url(r'^state/delete/(?P<state_id>\w+)/$', AssetState.delete, name='delete-asset-state'),
    #Goal
	url(r'^goal/$', Goal.index,name='goal'),
	url(r'^goal/add/(?P<parent_id>\w+)/$', Goal.add, name='add-goal'),
	url(r'^goal/edit/(?P<goal_id>\w+)/$', Goal.edit, name='edit-goal'),
	url(r'^goal/delete/(?P<goal_id>\w+)/$', Goal.delete, name='delete-goal'),
	#AssetVolatility
	url(r'^asset-volatility/$', AssetVolatility.index,name='asset-volatility'),
	url(r'^volatility/add/(?P<parent_id>\w+)/$', AssetVolatility.add, name='add-asset-volatility'),
	url(r'^volatility/edit/(?P<volatility_id>\w+)/$', AssetVolatility.edit, name='edit-asset-volatility'),
	url(r'^volatility/delete/(?P<volatility_id>\w+)/$', AssetVolatility.delete, name='delete-asset-volatility'),
    # Reason
    url(r'^reason/$', Reason.view_reason , name='reason'),
    url(r'^reason/add/$', Reason.add_reason, name='add-reason'),
    url(r'^reason/delete/(?P<reason_id>\w+)/$', Reason.delete_reason, name='delete-reason'),
    url(r'^reason/(?P<reason_id>\w+)/$', Reason.change_reason, name='change-reason'),
    #Join-Release_asset
    url(r'^release-asset/$', JoinReleaseAsset.release_asset, name='release_asset'),
    url(r'^join-asset/$', JoinReleaseAsset.join_asset, name='join-asset'),
    url(r'^get-child-asset/(?P<asset_parent_id>\w+)/$', JoinReleaseAsset.load_child_asset, name='get-child-asset'),
    url(r'^amortize-asset/$', AmortizeAsset.index, name='amortize-asset'),
    url(r'^asset-type/$', AssetType.index, name='asset-type'),
    url(r'^load-asset-detail/(?P<asset_id>\w+)/$', AssetType.load_asset_detail, name='load-asset-detail'),
    # Report
    url(r'^report/asset-inventory-report/$', Report.view_Asset_Inventory_report , name='asset-inventory-report'),
    url(r'^report/verify-asset-report/$', Report.verify_asset_report , name='verify-asset-report'),
    url(r'^report/asset-by-project-report/$', Report.asset_project_report , name='asset-by-project-report'),
    # Error page
)