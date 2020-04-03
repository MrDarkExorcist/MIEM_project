# coding: utf-8
# Импортирует поддержку UTF-8.

# Импортируем модули для работы с JSON и логами.
import json
import logging
import subprocess
import time
from datetime import date
import os.path
from pyudmx import pyudmx

def read_device1(n):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (n))
    line = f.readline()
    s=0
    count=0
    text=''
    while line:
        count+=1
        if count==1:
            text+="Номер девайса: "+line
            line = f.readline()
            continue
        if count==2:
            text+="Название: "+line
            line = f.readline()
            continue
        if count==3:
            text+="Каналы: "+line
            ch=int(line)
            line = f.readline()
            continue
        if count==4:
            text+="Старт : "+line
            sch=int(line)
            line = f.readline()
            s=1
            continue
        if count>(4+ch+ch):
            break
    f.close()
    return text

from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}



# Задаем параметры приложения Flask.

@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)

def get_suggests(id):
    session = sessionStorage[id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    return suggests

def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[0] = {
            'suggests': [
                "Запустить мастер контроль",
                "Журнал посещений",
                "Список подключенных устройств",
                "Текущее состояние приборов",
            ]
        }

        sessionStorage[1] = {
                'suggests': [
                    "Назад"
            ]
        }

        sessionStorage[2] = {
                'suggests': [
                    "Информация о приборе один",
                    "Информация о приборе два",
                    "Информация о приборе три",
                    "Информация о приборе четыре"
            ]
        }

        sessionStorage[3] = {
                'suggests': [
                    "Прибор 1",
                    "Прибор 2",
                    "Прибор 3",
                    "Прибор 4",
                "Назад"
            ]
        }

        sessionStorage[4] = {
            'suggests': [
                "Гость",
                "Авторизироваться",
            ]
        }
        res['response']['text'] = 'Приветсвую вас, это навык управления Осветительными DMX устройствами в МИЭМе. Чем я могу быть полезна?'
        res['response']['buttons'] = get_suggests(0)
        return
    if req['request']['original_utterance'].lower() in [
        'назад',
    ]:
        res['response']['text'] = 'Чем я могу помочь вам?'
        res['response']['buttons'] = get_suggests(0)
        return
    if req['request']['original_utterance'].lower() in [
        'журнал',
        'журнал посещений',
    ]:
        f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/log.txt","r")
        journal=f.read()
        f.close()
        res['response']['text'] = journal
        res['response']['buttons'] = get_suggests(1)
        return
    if req['request']['original_utterance'].lower() in [
        'список устройств',
        'список подключенных устройств',
    ]:
        num=0
        while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
            num+=1
        res['response']['text'] = "Найденой устройств: %d" % (int(num))
        res['response']['buttons'] = get_suggests(3)
        return
    if req['request']['original_utterance'].lower() in [
        'прибор 1',
        'прибор 2',
        'прибор 3',
        'прибор 4',
        'прибор 5',
        'прибор 6',
        'прибор 7',
        'прибор 8',
        'прибор 9',
        'прибор 10',
    ]:
        name=req['request']['original_utterance'].lower()
        if os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%s" % (name[-1:])):
            res['response']['text'] = read_device1(int(name[-1:]))
            res['response']['buttons'] = get_suggests(3)
        else:
            res['response']['text'] = "Устройство не найдено."
            res['response']['buttons'] = get_suggests(3)
        return

if __name__ == '__main__':
    app.run()