from datetime import datetime
import json

from django.http import HttpResponse


def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        raise TypeError(repr(obj) + " is not JSON serializable")


def render_json(data):
    response = HttpResponse(json.dumps(data, default=datetime_handler),
                            content_type='application/json')
    response['Cache-Control'] = 'no-cache'
    response['Pragma'] = 'no-cache'
    return response
