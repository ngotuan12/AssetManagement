# -*- coding: utf-8 -*-
'''
Created on Apr 3, 2014

@author: TuanNA
'''
# @login_required(login_url='/signin')

from myapp.models import mybarcode
from AssetWebapp import settings

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from myapp.models.StockAssetSerial import StockAssetSerial
@login_required(login_url='/login/')
def print_asset(request,asset_id):
        stockAssetSerial = StockAssetSerial.objects.get(id=asset_id)
        #create bảcode
        serial =stockAssetSerial.serial
        d = mybarcode.MyBarcodeDrawing(serial)
        d.save(formats=['png'],outDir=settings.REPORT_ROOT,fnRoot=serial)
        
        context={"stockAssetSerial":stockAssetSerial,"serial":serial}
        return render_to_response("invoice.html", context, RequestContext(request))