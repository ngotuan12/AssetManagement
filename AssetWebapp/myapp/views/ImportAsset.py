# -*- coding: utf-8 -*-
'''
Created on Oct 22, 2014

@author: TuanNA
'''
import json
import os

from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from AssetWebapp.settings import UPLOAD_ROOT
from myapp.importer.DepartmentImporter import DepartmentImporter
from sc.util.base import handle_uploaded_file


def index(request):
    context = {}
    if request.POST:
        importer = DepartmentImporter(file_path="D:\import.xls", import_type=2)
        importer.do_import()
    return render_to_response("asset/import-asset.html", context, RequestContext(request))
def upload(request):
    if request.method == 'POST':
        try:
            fileName,fileExtension = os.path.splitext(request.FILES['file-input'].name)
            if not fileExtension==".xls":
                raise Exception(_(u"Định dạng file phải là excel!"))
            uploaded_file = handle_uploaded_file(request.FILES['file-input'])
            return HttpResponse("""
                                <form id='form-uploaded'> <p style="color: #636e7b;"> %s </p> 
                                    <input id="uploaded-file" name="uploaded-file" type="hidden" value="%s"/>
                                </form>
                                """
                                % (_(u"Bạn đang chọn file <strong>%s</strong> ")% fileName,uploaded_file))
        except Exception as ex:
            return HttpResponse(str(ex))
def test_import(request):
    if request.method == 'POST':
        file_name = request.POST["uploaded-file"]
        try:
            importer = DepartmentImporter(file_path=UPLOAD_ROOT + "/" + file_name, import_type=2)
            log_file = importer.do_test()
            return HttpResponse(json.dumps({"handle":"success","log_file":log_file}) ,content_type="application/json")
        except Exception as ex:
            return HttpResponse(json.dumps({"handle":"error", "message": str(ex)}),content_type="application/json")
    