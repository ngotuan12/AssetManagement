# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseRedirect

from myapp.models import mybarcode
from AssetWebapp import settings


def barcode(request):
    #instantiate a drawing object
    code = '1231245fgdfgdf'
    d = mybarcode.MyBarcodeDrawing(code)
    d.save(formats=['png'],outDir=settings.REPORT_ROOT,fnRoot=code)
    binaryStuff = d.asString('gif')
    return HttpResponseRedirect("/report/"+code+".png")
