'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

from myapp.models import Area


@login_required(login_url='/login')
def index(request):
	try:
		lsArea = Area.objects.all()
		context={'lsArea':lsArea}
		context.update(csrf(request))
	except Exception as ex:
		context={}
		print(ex)
	finally:
		return render_to_response("area.html", context)