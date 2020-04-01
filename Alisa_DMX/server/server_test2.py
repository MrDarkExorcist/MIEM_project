# coding: utf-8
# Импортирует поддержку UTF-8.

# Импортируем модули для работы с JSON и логами.
import json
import logging

from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/post", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    #logging.info('Request: %r', request.json) #Логи для консоли. От пользователя

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)
    #logging.info('Response: %r', response) #Логи для консоли. От программы

    return json.dumps(response)

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Нет.",
                "Это неправильно.",
                "Пересчитай!",
            ]
        }

        res['response']['text'] = 'Привет! 2+2 равно 5?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'да',
        'наверное',
        'может быть',
        'согласен',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'А я тебя обманула! :)'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Многие говорят "%s", но я говорю правду!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку с картинкой.
    if len(suggests) < 2:
        suggests.append({
            "title": "Я верю, но докажи",
            "url": "https://ru-static.z-dn.net/files/d53/04459eacfcaa734be7bad9460a8f6bca.jpg",
            "hide": True
        })

    return suggests

if __name__ == '__main__':
    app.run()