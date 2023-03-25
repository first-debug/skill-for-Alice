import json
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .functions import *


@csrf_exempt
def post(request):
    req = json.loads(request.body.decode('utf-8'))
    response = {
        'session': req['session'],
        'version': req['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, req)
    return HttpResponse(json.dumps(response))