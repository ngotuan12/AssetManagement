'''
Created on Apr 3, 2014

@author: TuanNA
'''
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from myapp.models.Device import Device
from myapp.models.DeviceInfor import DeviceInfor


@login_required(login_url='/login')
@require_http_methods(["POST",])
@permission_required('myapp.view_deviceproperties',login_url='/permission-error')
def index(request):
	try:
		device_id=request.POST['device_id']
		device = Device.objects.get(id=device_id)
		device_infor= DeviceInfor.objects.filter(device_id=device,status='1').select_related().order_by('device_pro__code')
		print(device_infor.query)
		infors =[]
		for infor in device_infor:
			infors.append({'id':infor.id,'value':infor.value,'status':infor.status,'properties':model_to_dict(infor.device_pro)})
		return HttpResponse(json.dumps({'device_infor':infors,'device':model_to_dict(device)}) ,content_type="application/json")
	except Exception as ex:
		return HttpResponse(json.dumps({"error": str(ex)}),content_type="application/json")