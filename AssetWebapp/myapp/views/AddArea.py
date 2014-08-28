# -*- coding: utf8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models import Area


@login_required(login_url='/login')
@permission_required('myapp.add_area',login_url='/permission-error')
def index(request):
	if request.method == 'GET':
		try:
			lsArea = Area.objects.all()
			context={'lsArea':lsArea}
			context.update(csrf(request))
		except Exception as ex:
			context={}
			print(ex)
		finally:
			return render_to_response("add-area.html", context,RequestContext(request))
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == "addArea":
			context={}
			try:
				_code = request.POST['txtCode'].strip()
				_name = request.POST['txtName'].strip()
				_lat = request.POST['txtLat'].strip()
				_lng = request.POST['txtLng'].strip()
				_status = request.POST['slStatus'].strip()
				area = Area.objects.filter(code = _code.upper())
				if len(area) >0 :
					raise Exception(("Mã khu vực '").decode('utf-8')+ _code + ("' đã tồn tại").decode('utf-8'))
				else :
					
					parent = Area.objects.get(code = 'VN')
					area = Area()
					
					area.code = _code.upper()
					area.name = _name
					area.parent = parent
					area.lat = float(_lat)
					area.lng = float(_lng)
					area.status = _status
					area.level = '2'
					area.type = '2'
					
					area.save()
				#get data show client
				lsArea = Area.objects.all()
				context={'lsArea':lsArea}
				context.update(csrf(request))
				return HttpResponseRedirect('/area')
			except Exception as ex:
				context.update({'has_error':ex,'code':_code,'name':_name,'status':_status,'lat':_lat,'lng':_lng})
				context.update(csrf(request))
				return render_to_response("add-area.html", context,RequestContext(request))
