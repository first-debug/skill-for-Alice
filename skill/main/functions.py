from random import choice
from django.core.exceptions import ObjectDoesNotExist
from main.models import Heroes, Answer


def init_varabls():
    global help_command, start_phrase, heroes_names
    help_command = {'умеешь', 'помощь', 'помоги', 'напомни'}
    start_phrase = {'поделись', 'рассказать', 'узнать', 'знаешь', 'расскажи', 'информация', 'поведуй'}
    heroes_names = set()
    for i in Heroes.objects.all():
        heroes_names |= set(i.possible_name.split())


def handle_dialog(res, req):

    # если пользователь только что запустил навык, то выводим информацию о навыке
    if req['session']['new']:
        res['response']['text'] = choice(Answer.objects.filter(type_ans='start')).text
        return
    
    input_text = set(req['request']['nlu']['tokens'])
    
    if help_command & input_text:
        res['response']['text'] = choice(Answer.objects.filter(type_ans='start')).text
    
    elif start_phrase & input_text:
        if heroes_names & input_text:
            for i in Heroes.objects.all():
                name = ' '.join([i for i in heroes_names & input_text])
                if name in i.possible_name:
                    res['response']['text'] = f'{i.id}; {i.name.title()}; {i.primary_attr.capitalize()}'
                    break
                else:
                    res['response']['text'] = 'beee((('
        else:
            res['response']['text'] = 'go to fix, mather fucker'

    else:
        res['response']['text'] = 'NO true ifs'
    