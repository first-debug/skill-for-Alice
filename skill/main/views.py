import json
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint

from .functions import *


@csrf_exempt
def post(request):
    init_varabls()
    req = json.loads(request.body.decode('utf-8'))
    response = {
        'session': req['session'],
        'version': req['version'],
        'response': {
            'end_session': False
        }
    }
    # db_actions()
    handle_dialog(response, req)
    return HttpResponse(json.dumps(response))
