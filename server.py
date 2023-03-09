# импортируем библиотеки
from flask import Flask, request
import logging
import json

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
hist = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new'] or hist[req['session']['session_id']] == 'Кролика':
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = f'''Купи {hist[req['session']['session_id']].lower()}!'''
        if req['session']['new']:
            hist[req['session']['session_id']] = 'Слона'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ] or any([i in ['ладно', 'куплю', 'покупаю', 'хорошо'] for i in req['request']['nlu']['tokens']]):
        res['response']['text'] = f'''{hist[req['session']['session_id']]} можно найти на Яндекс.Маркете!'''
        if hist[req['session']['session_id']] == "Кролика":
            res['response']['end_session'] = True
        else:
            hist[req['session']['session_id']] = 'Кролика'
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {hist[req['session']['session_id']].lower()}!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
