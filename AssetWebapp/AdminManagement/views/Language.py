'''
Created on Oct 2, 2014

@author: TuanNA
'''
from django.http.response import HttpResponseRedirect
# from django.shortcuts import render_to_response


def switch_language(request,language_code):
    request.session['django_language'] = language_code
    request.session['_language'] = language_code
#     response = render_to_response()
#     response.set_cookie('django_language',language_code)
    if request.GET.has_key('next'):
        return HttpResponseRedirect(request.GET['next'])
    return  HttpResponseRedirect("/home/");