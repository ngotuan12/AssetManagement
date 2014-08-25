# -*- coding: utf8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from myapp.models import Area


@login_required(login_url='/login')
def index(request):
	if request.method == 'GET':
		try:
			_area_id = request.GET['area_id']
			area = Area.objects.get(id = _area_id)
			context={'area':area}
			
			context.update(csrf(request))
		except Exception as ex:
			context={}
			print(ex)
		finally:
			return render_to_response("edit-area.html", context)
	elif request.method == 'POST':
		formType= request.POST['type']
		if formType == "editArea":
			context={}
			try:
				_area_id = request.POST['area_id'].strip()
				_code = request.POST['txtCode'].strip()
				_name = request.POST['txtName'].strip()
				_lat = request.POST['txtLat'].strip()
				_lng = request.POST['txtLng'].strip()
				_status = request.POST['slStatus'].strip()
				area = Area.objects.filter(code = _code.upper())
				if len(area) >1 :
					raise Exception(("Mã khu vực '").decode('utf-8')+ _code + ("' đã tồn tại").decode('utf-8'))
				elif len(area) == 1:
					if str(_area_id) != str(area[0].id) :
						raise Exception(("Mã khu vực '").decode('utf-8')+ _code + ("' đã tồn tại").decode('utf-8'))
				else :
					area = Area.objects.get(id = _area_id)
					
					area.code = _code
					area.name = _name
					area.lat = float(_lat)
					area.lng = float(_lng)
					area.status = _status
					area.level = '2'
					area.type = '2'
					
# 					area.save()
				#get data show client
				lsArea = Area.objects.all()
				context={'lsArea':lsArea}
				context.update(csrf(request))
				return HttpResponseRedirect('/area')
			except Exception as ex:
				context.update({'has_error':ex,'area_id':_area_id,'code':_code,'name':_name,'status':_status,'lat':_lat,'lng':_lng})
				context.update(csrf(request))
				return render_to_response("edit-area.html", context)
