from random import choice
from django.core.exceptions import ObjectDoesNotExist


def handle_dialog(res, req):

    # если пользователь только что запустил навык, то выводим информацию о навыке
    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу ответить на интересующие тебя вопросы, такие как: информацию о героях, предметах и скиллах, а также помогу определиться со ' \
        'сборкой предметов на любого интересующего тебя героя. Какой вопрос вас интересует?'
        return
    
    if 'расскажи мне о' in req['request']['command']:
        pass
