# -*- coding:utf8 -*-
import logging

import simplejson as json

from contrib.shortcuts import json_response


def server_error_404(request):
    return json_response({'ret':False,'msg':u'找不到指定页面','code':1002})

def server_error_500(request):
    return json_response({'ret':False,'msg':u'系统错误','code':1000})