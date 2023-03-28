from random import choice
import json
from main.models import Items, Heroes, Answer, UserData, NewPossibleNames


def init_varabls():
    global help_command, start_phrase, heroes_names, negative_ans, positive_ans  #, items_names, abilities
    help_command = {'умеешь', 'помоги', 'напомни', 'можешь'}
    start_phrase = {'поделись', 'рассказать', 'узнать', 'знаешь', 'расскажи', 'информация', 'поведуй'}
    heroes_names, items_names, abilities, negative_ans, positive_ans = set(), set(), set(), set(), set()
    for i in Heroes.objects.all():
        heroes_names |= set(i.possible_name.split())
    # for i in Items.objects.all():  # !!!!!
    #     items_names |= set(i.possible_name.split())
    # for i in Items.objects.all():  # !!!!!
    #     abilities |= set(i.possible_name.split())
    for i in Answer.objects.filter(type_ans='positive'):
        positive_ans |= set(i.text.split())
    for i in Answer.objects.filter(type_ans='negative'):
        negative_ans |= set(i.text.split())



def handle_dialog(res, req):
    if req['session']['user']:
        user_id = req['session']['user']['user_id']
        if not UserData.objects.filter(pk=user_id):
            UserData(user_id=user_id).save()
    else:
        user_id = req['session']['application']['application_id']
        if not UserData.objects.filter(pk=user_id):
            UserData(user_id=user_id).save()
    
    if req['session']['new']:
        res['response']['buttons'] = []
        res['response']['text'] = choice(Answer.objects.filter(type_ans='start')).text
        user = UserData.objects.filter(pk=user_id)[0]
        if user.recent_names:
            for i in user.recent_names.split(','):
                if i:
                    res['response']['buttons'].append({
                        "title": i.split(':')[1].title(),
                        "payload": {
                            "type": i.split(':')[0],
                            "name": i.split(':')[1]
                                    },
                        'hide':True
                        })
        return
    
    input_text = set(req['request']['nlu']['tokens'])
    print(input_text)
    try:
        payload = req['request']['payload']['type']
    except KeyError:
        payload = None

    if help_command & input_text:
        res['response']['text'] = choice(Answer.objects.filter(type_ans='start')).text
    
    elif {'помощь', } & input_text:
        res['response']['text'] = choice(Answer.objects.filter(type_ans='help')).text
    
    elif start_phrase & input_text or payload:
        if heroes_names & input_text:
            input_name = ' '.join([i for i in heroes_names & input_text])

            for i in Heroes.objects.all():
                if input_name in i.possible_name:
                    user = UserData.objects.get(pk=user_id)
                    user.count_unrec = 0
                    res['response']['text'] = f'{i.name.title()}:\n-Основной атрибут: {i.primary_attr.capitalize()}\n-Тип атаки: {i.attack_type}\n-Стартовый урон: ' \
                        f'{i.start_damage}\n-Стартовое здоровье: {i.start_health}\n-Регенирация здоровья в начале: {i.start_health_regen}\n-Стартовая мана: {i.start_mana}\n' \
                            f'-Регенирация маны в начале: {i.start_mana_regen}\n-Стартовый армор: {i.start_armor}\n-Скоротсь атаки в начале: {i.start_attack_speed}' \
                                f'\n\n{choice(Answer.objects.filter(type_ans="after_desc")).text}'
                    res['response']['buttons'] = [{
                        "title": choice(Answer.objects.filter(type_ans='positive')).text.title(),
                        'hide':True
                        },
                        {
                        "title": choice(Answer.objects.filter(type_ans='negative')).text.title(),
                        'hide':True
                        },
                        {
                        "title": 'Покажи картинку',
                        'payload': {'type': '',
                                    'hero': i.name},
                        'hide':True
                        }]
                    if f'hero:{i.name}' not in user.recent_names:
                        user.recent_names += f'hero:{i.name},'
                        recent_names = user.recent_names
                        print(recent_names.split(','))
                        if len(recent_names.split(',')) > 6:
                            user.recent_names = recent_names[recent_names.index(',') + 1:]
                    user.save()
                    return
        else:
            res['response']['text'] = 'Если вы ввели название предмета или способности, то, к сожелению, мы ещё не успели занести всю необходимую информацию. Если вы ввели' \
                 ' корректное имя персонажа в какой-то иной форме, то мы просто не учли его. Введите "add_hero;корректное имя на английском;имя, которое вы ввели" для того' \
                     ' чтоб мы смогли добавить это имя. Зарание спасибо!'

    elif positive_ans & input_text:
        res['response']['buttons'] = []
        res['response']['text'] = f"{choice(Answer.objects.filter(type_ans='start')).text}\nP.S. тут в будущем изменим текст на более логичный"
        user = UserData.objects.filter(pk=user_id)[0]
        if user.recent_names:
            for i in user.recent_names.split(','):
                if i:
                    res['response']['buttons'].append({
                        "title": i.split(':')[1].title(),
                        "payload": {
                            "type": i.split(':')[0],
                            "name": i.split(':')[1]
                                    },
                        'hide':True
                        })

    elif negative_ans & input_text:
        res['response']['text'] = choice(Answer.objects.filter(type_ans='end')).text
        res['response']['end_session'] = True

    elif {'покажи', 'картинку'} == input_text:
                    res['response']['buttons'] = [{
                        "title": choice(Answer.objects.filter(type_ans='positive')).text.title(),
                        'hide':True
                        },
                        {
                        "title": choice(Answer.objects.filter(type_ans='negative')).text.title(),
                        'hide':True
                        }]
                    res['response']['text'] = req['request']['payload']['hero'].title()
                    res['response']['card'] = {}
                    res['response']['card']['type'] = 'BigImage'
                    res['response']['card']['title'] = choice(Answer.objects.filter(type_ans='after_desc')).text
                    res['response']['card']['image_id'] = Heroes.objects.get(name=req['request']['payload']['hero']).image_id

    elif 'add_hero' in req['request']['original_utterance']:
        _, possible, current = req['request']['original_utterance'].split(';')
        NewPossibleNames(name=current, possible_name=possible).save()
        res['response']['text'] = 'Спасибо!\nПродолжим?'
        res['response']['buttons'] = [{
                        "title": choice(Answer.objects.filter(type_ans='positive')).text.title(),
                        'hide':True
                        },
                        {
                        "title": choice(Answer.objects.filter(type_ans='negative')).text.title(),
                        'hide':True
                        }]

    else:
        user = UserData.objects.get(pk=user_id)
        if user.count_unrec < 3:
            user.count_unrec += 1
        user.save()
        res['response']['text'] = choice(Answer.objects.filter(type_ans=f'unrec_{user.count_unrec}')).text
    

def db_actions():
    with open('items.json', 'r', encoding='utf-8') as file:
        file = json.loads(file.read())
        for i in Items.objects.all():
            i.name
