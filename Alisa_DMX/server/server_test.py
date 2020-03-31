from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def main():
    ## Ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполнение информации
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    if req['request']['original_utterance']:
        ## Проверка содержимого
        res['response']['text'] = req['request']['original_utterance']
        print("Ответ отправлен.")
    else:
        ## Если первое сообщение
        res['response']['text'] = "Тестовый навык. Эхобот"

if __name__ == '__main__':
    app.run()