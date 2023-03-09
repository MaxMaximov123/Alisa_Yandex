# импортируем библиотеки
from flask import Flask, request
import logging
import json

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)
sessionStorage = {}
st = ['Слона', 0]


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
    global sessionStorage
    user_id = req['session']['user_id']

    if req['session']['new'] or st[1]:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = f'Привет! Купи {st[0].lower()}!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ] or any([i in ['ладно', 'куплю', 'покупаю', 'хорошо'] for i in req['request']['nlu']['tokens']]):
        if st[1]:
            res['response']['end_session'] = True
            res['response']['text'] = f'{st[0]} можно найти на Яндекс.Маркете!'
        else:
            res['response']['text'] = f'{st[0]} можно найти на Яндекс.Маркете!\nКупи {"Кролика"}'
            st[0] = 'Кролика'
            st[1] = 1
            sessionStorage[user_id] = {
                'suggests': [
                    ''
                    "Не хочу.",
                    "Не буду.",
                    "Отстань!",
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {st[0].lower()}!"
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
            "url": f"https://market.yandex.ru/search?text={st[0]}",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
