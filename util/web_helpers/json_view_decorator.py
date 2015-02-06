# -*- encoding=utf-8 -*-

from functools import wraps
import datetime

from django.http import HttpResponse
from django.utils import simplejson as json


def object_queryset_to_dict(obj_queryset):
    if obj_queryset.has_key('create'):
        obj_queryset['create'] = obj_queryset['create'].strftime('%Y-%m-%d %H:%M:%S')
    return obj_queryset

def to_dict(obj):
    fields = []
    for field in obj._meta.fields:
        fields.append(field.name)
    d = {}
    for attr in fields:
        if type(getattr(obj, attr)) == type(datetime.datetime.now()):
            d[attr] = getattr(obj, attr).strftime('%Y-%m-%d %H:%M:%S')
        else:
            d[attr] = getattr(obj, attr)
    return d

def render_to_json(**jsonargs):
    """
    Renders a JSON response with a given returned instance. Assumes json.dumps() can
    handle the result. The default output uses an indent of 4.

    @render_to_json()
    def a_view(request, arg1, argN):
        ...
        return {'x': range(4)}

    @render_to_json(indent=2)
    def a_view2(request):
        ...
        return [1, 2, 3]

    """
    def outer(f):
        @wraps(f)
        def inner_json(request, *args, **kwargs):
            result = f(request, *args, **kwargs)
            r = HttpResponse(mimetype='application/json')
            if result:
                indent = jsonargs.pop('indent', 4)
                r.write(json.dumps(result, indent=indent, **jsonargs))
            else:
                r.write("{}")
            return r
        return inner_json
    return outer

