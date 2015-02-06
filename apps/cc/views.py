# -*- coding:utf8 -*-
import logging
import datetime
import hashlib
import uuid
import os

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
import simplejson as json

from annoying.decorators import render_to
from apps.cc.models import Files
from settings import CURRENT_PATH

imgs = ['jpg','png','gif']
excel = ['xls']
txt = ['txt']


def api(request):
    if request.method == 'POST':
        f = request.FILES.get('upload_file','')
        ret = __file_upload(f)
        if ret[1]:
            __into_database(ret[1])
            return HttpResponse(json.dumps({'ret':True,'data':'http://112.124.100.205/static/upload/'+ret[1]}))
        else:
            return HttpResponse(json.dumps({'ret':False,'msg':u'上传失败'}))
    files = [{'url':k.url,'create':k.create.strftime('%Y-%m-%d %H:%M:%S')}for k in Files.objects.all()]
    return HttpResponse(json.dumps({'ret':True,'data':files}))

@render_to('cc/index.html')
def index(request):
    if request.method == 'POST':
        type = request.REQUEST.get('type','all')
        size = request.REQUEST.get('size','')
        if not size:
            size = 0
        try:
            size = int(size)
        except Exception,e:
            messages.error(request, u'请输入正确的数字格式')

        f = request.FILES.get('upload_file','')
        if f:
            bool_upload = True
            f_name = f.name.split('.')[-1]
            f_size = f.size/1024

            if type == 'imgs':
                if f_name not in imgs:
                    bool_upload = False
                    messages.error(request, u'请上传图片')
            if type == 'xls':
                if f_name not in excel:
                    bool_upload = False
                    messages.error(request, u'请上传excle')
            if type == 'txt':
                if f_name not in txt:
                    bool_upload = False
                    messages.error(request, u'请上传txt')
            if size != 0:
                if f_size > size:
                    bool_upload = False       
                    messages.error(request, u'上传文件大小超过限制')
            if bool_upload:
                ret = __file_upload(f)
                if ret[1]:
                    __into_database(ret[1])
                    messages.success(request, u'上传成功')
                else:
                    messages.error(request, u'上传失败')
        else:
            messages.error(request, u'请选择要上传的文件')

    page = int(request.REQUEST.get('page',1))
    files = Files.objects.all()
    paginator = Paginator(files, 20)
    try:
        files = paginator.page(page)
    except Exception,e:
        logging.error(e)
        files = paginator.page(paginator.num_pages)

    return {
        'page':page,
        'files':files,
    }

def delete(request,id):
    f = Files.objects.get(id=id).delete()
    messages.success(request, u'删除成功')
    return HttpResponseRedirect('/')

def __into_database(url):
    f = Files()
    f.url = url
    f.save()

    return True

def __file_upload(f):
    if f:
        path=os.path.join(CURRENT_PATH,'static/upload')
        file_name=str(uuid.uuid4().hex)+"."+str(f.name.split('.').pop())
        path_file=os.path.join(path,file_name)
        try:
            file = open(path_file, 'wb' )
            f_data = f.read()
            file.write(f_data)
            file.close()
            return (True,file_name)
        except:
            return (False,'')
    return (False,'')