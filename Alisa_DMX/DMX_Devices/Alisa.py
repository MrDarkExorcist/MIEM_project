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

def scan(n):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (n))
    line = f.readline()
    value = []
    count=0
    ch=100
    sch=-1
    while line:
        count+=1
        if count==3:
            ch=int(line)
            line = f.readline()
            continue
        if count==4:
            sch=int(line)
            line = f.readline()
            continue
        if count>(4+ch+ch):
            break
        if count>4 and count%2==0:
            value.append(int(line))
            line = f.readline()
            continue
        line = f.readline()
    f.close()
    return(sch,value)

def device_dump(number, channels, value, start):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % number)
    namefile1='device_%d_new' % (number)
    namefile2='device_%d_сh_%d_new' % (number, channels)
    for i in range(3):
        line = f.readline()
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile1), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile2), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    subprocess.call("echo '%d' >> '%s'" % (start,namefile1), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("echo '%d' >> '%s'" % (start,namefile2), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    for i in range(channels):
        line = f.readline()
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile1), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile2), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
        line = f.readline()
        subprocess.call("echo '%d' >> '%s'" % (value[i],namefile1), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
        subprocess.call("echo '%d' >> '%s'" % (value[i],namefile2), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    subprocess.call("rm 'device_%d'" % (number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("mv '%s' 'device_%d'" % (namefile1, number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("rm 'device_%d_ch_%d'" % (number, channels), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    subprocess.call("mv '%s' 'device_%d_ch_%d'" % (namefile2, number, channels), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    f.close()
    return

def device_load(number, channels):
    subprocess.call("rm 'device_%d'" % (number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("cp 'device_%d_ch_%d' '/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d'" % (number, channels, number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    return

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
        if count>4:
            break
    f.close()
    return text

def find_ch_n(n, d):
        f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (n))
        line = f.readline()
        fl=True
        s=-1
        count=0
        subcount=0
        while line:
            count+=1
            if count>4:
                subcount+=1
                if subcount%2==1 and subcount//2==d-1:
                    answer=line
                    fl=False
                    break
            line = f.readline()
        f.close()
        if fl:
            return("Канал не найден")
        else:
            return(answer)

from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)


# Хранилище данных о сессиях.
sessionStorage = {}
UserInfo = {}

User_dev={}
User_ch={}
User_s={}
User_val={}

sessionStorage[0] = {
            'suggests': [
                "Запустить мастер контроль",
                "Журнал посещений",
                "Список подключенных устройств",
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
                "все приборы конфигурация",
                "все приборы проверка",
                "прибор 1 канал 1 инфо",
                "прибор 1 стартовый канал инфо",
                "прибор 1 стартовый канал отправь 1",
                "прибор 1 сброс",
                "прибор 1 канал 1 отправь 1",
                "Журнал посещений",
                "Журнал действий",
                "Список подключенных устройств",
                "Закончить"
            ]
        }
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
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]
    return suggests

def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        UserInfo[user_id] = 0 
        res['response']['text'] = 'Приветсвую вас, это навык управления Осветительными DMX устройствами в МИЭМе. Чем я могу быть полезна?'
        res['response']['buttons'] = get_suggests(0)
        return    
    if UserInfo[user_id] == 0:
        if req['request']['original_utterance'].lower() in [
        'журнал посещений',
    ]:
            f=open("/home/pi/Alisa_DMX/server/log_а.txt","r")
            journal=f.read()
            journal = [i for i in journal.split('\n')]
            journal = journal[-5:]
            journal = '\n'.join(journal)
            journal = "Последние 5 записей:\n"+journal
            res['response']['text'] = journal
            res['response']['buttons'] = get_suggests(1)
            return
        elif req['request']['original_utterance'].lower() in [
        'список устройств',
        'список подключенных устройств',
    ]:
            num=0
            while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
                num+=1
            res['response']['text'] = "Найденой устройств: %d" % (int(num))
            res['response']['buttons'] = get_suggests(3)
            return
        elif req['request']['original_utterance'].lower() in [
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
        elif req['request']['original_utterance'].lower().find("мастер контроль")>=0:
            res['response']['text'] = "Для начала, я попрошу вас авторизироваться. Если у вас нет аккаунта, обратитесь к администратору. Введите свои почту/пароль в формате:\nmail@miem.hse.ru|password"
            return
        elif req['request']['original_utterance'].lower() in [
        'назад',
        '',
        ]:
            res['response']['text'] = 'Чем я могу быть полезна?'
            res['response']['buttons'] = get_suggests(0)
            return
        elif req['request']['original_utterance'].lower().find("@miem.hse.ru|")>=0:
            f=open("/home/pi/Alisa_DMX/server/log_pas.txt","r")
            line = f.readline()
            while line:
                if line==req['request']['original_utterance']:
                    UserInfo[user_id] = 1
                    num=0
                    User_s[user_id]=[]
                    User_val[user_id]=[]
                    User_ch[user_id]=[]
                    User_dev[user_id]=pyudmx.uDMXDevice()
                    User_dev[user_id].open()
                    while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
                        num+=1
                    for j in range(num):
                        s, val=scan(j+1)
                        User_s[user_id].append(s)
                        User_val[user_id].append(val)
                        User_ch[user_id].append(len(val))
                    d=0
                    for i in User_s[user_id]:
                        d+=1
                    res['response']['text'] = "Рада вас видеть снова!\nЗагружено устройств: %d\nКонфигурация завершена" % d
                    res['response']['buttons'] = get_suggests(1)
                    f.close()
                    subprocess.call("echo '%s %s %s %s' >> 'log_а.txt'" % (time.strftime("%H:%M:%S"),date.today(),user_id,line[:-5]), shell=True,cwd='/home/pi/Alisa_DMX/server/')
                    return
                line = f.readline()
            if UserInfo[user_id] == 0:
                res['response']['text'] = "Простите, такого пользователя не обнаружено. Проверьте правильность ввода или обратитесь к администратору."
            f.close()
            return
        else:
            res['response']['text'] = "Команда не опознана или у вас не полномочий" 
            res['response']['buttons'] = get_suggests(1)
    if UserInfo[user_id] == 1:
        if req['request']['original_utterance'].lower() in [
        'назад',
    ]:
            res['response']['text'] = 'Чем я могу быть полезна? (Мастер контроль)'
            res['response']['buttons'] = get_suggests(4)
            return    
        elif req['request']['original_utterance'].lower() in [
        'журнал посещений',
    ]:
            f=open("/home/pi/Alisa_DMX/server/log_а.txt","r")
            journal=f.read()
            journal = [i for i in journal.split('\n')]
            journal = journal[-5:]
            journal = '\n'.join(journal)
            journal = "Последние 5 записей:\n"+journal
            res['response']['text'] = journal
            res['response']['buttons'] = get_suggests(1)
            return
        elif req['request']['original_utterance'].lower() in [
        'журнал действий',
    ]:
            f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/log_online.txt","r")
            journal=f.read()
            journal = [i for i in journal.split('\n')]
            journal = journal[-5:]
            journal = '\n'.join(journal)
            journal = "Последние 5 записей:\n"+journal
            res['response']['text'] = journal
            res['response']['buttons'] = get_suggests(1)
            return
        elif req['request']['original_utterance'].lower() in [
        'список устройств',
        'список подключенных устройств',
    ]:
            num=0
            while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
                num+=1
            res['response']['text'] = "Найденой устройств: %d" % (int(num))
            res['response']['buttons'] = get_suggests(3)
            return
        elif req['request']['original_utterance'].lower() in [
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
        elif req['request']['original_utterance'].lower().find("все приборы")>=0 and req['request']['original_utterance'].lower().find("проверка")>=0:
            subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            check=0
            text=''
            flag=False
            for i in range(len(User_s[user_id])-1):
                check+=User_ch[user_id][i]+User_s[user_id][i]
                if User_s[user_id][i+1]<check:
                    text+=("Конфликт приборов %d %d\n" % (i+1, i+2))
                    flag=True
                check=0
            if flag:
                text+="Переобозначьте стартовые каналы!"
            else:
                text+="Конфликтов не обнаружено."
            res['response']['text'] = text
            res['response']['buttons'] = get_suggests(1)
            return
        elif req['request']['original_utterance'].lower().find("все приборы")>=0 and req['request']['original_utterance'].lower().find("конфигурация")>=0:
                subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                User_s[user_id]=[]
                User_val[user_id]=[]
                User_ch[user_id]=[]
                num=0
                while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
                    num+=1
                for j in range(num):
                    s, val=scan(j+1)
                    User_s[user_id].append(s)
                    User_val[user_id].append(val)
                    User_ch[user_id].append(len(val))
                res['response']['text'] = "Все каналы сброшены"
                res['response']['buttons'] = get_suggests(1)
                return
        elif req['request']['original_utterance'].lower().find("стартовый канал")>=0 and req['request']['original_utterance'].lower().find("прибор")>=0:
            if req['request']['original_utterance'].lower().find("инфо")>=0:
                subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                resul = [i for i in req['request']['original_utterance'].lower().split() if i.isdigit()]
                resul = ''.join(resul)
                resul = int(resul)
                if resul >= 1 and resul <= len(User_s[user_id])+1:
                    ans, buf=scan(resul)
                    res['response']['text'] = "Стартовый канал прибора: %s" % (str(ans))
                    res['response']['buttons'] = get_suggests(1)
                    return
                else:
                    res['response']['text'] = "Прибор не найден"
                    res['response']['buttons'] = get_suggests(1)
                    return
            elif req['request']['original_utterance'].lower().find("отправь")>=0:
                subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = req['request']['original_utterance'].lower().find("прибор")
                mid = req['request']['original_utterance'].lower().find("канал")
                res1 = req['request']['original_utterance'].lower()[beg:mid]
                res2 = req['request']['original_utterance'].lower()[-8:]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                if res1 >= 1 and res1 <= len(User_s[user_id])+1:
                    User_s[user_id][res1-1]=res2
                    res['response']['text'] = "Стартовый канал сменен на %d" % res2
                    res['response']['buttons'] = get_suggests(1)
                    return
                else:
                    res['response']['text'] = "Прибор не найден"
                    res['response']['buttons'] = get_suggests(1)
                    return
        elif req['request']['original_utterance'].lower().find("канал")>=0 and req['request']['original_utterance'].lower().find("прибор")>=0:
            if req['request']['original_utterance'].lower().find("инфо")>=0:
                subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = req['request']['original_utterance'].find("прибор")
                mid = req['request']['original_utterance'].find("канал")
                end = req['request']['original_utterance'].find("инфо")
                res1 = req['request']['original_utterance'][beg:mid]
                res2 = req['request']['original_utterance'][mid:end]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                if res1 >= 1 and res1 <= len(User_s[user_id])+1 and res2 >=1:
                    res['response']['text'] = find_ch_n(res1,res2)
                    res['response']['buttons'] = get_suggests(1)
                    return
                else:
                    res['response']['text'] = "Канал или устройство не найдены"
                    res['response']['buttons'] = get_suggests(1)
                    return
            elif req['request']['original_utterance'].lower().find("отправь")>=0:
                subprocess.call("echo '%s %s %s' >> 'log_online.txt'" % (time.strftime("%H:%M:%S"),date.today(),req['request']['original_utterance']), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = req['request']['original_utterance'].lower().find("прибор")
                mid = req['request']['original_utterance'].lower().find("канал")
                end = req['request']['original_utterance'].lower().find("отправь")
                res1 = req['request']['original_utterance'][beg:mid]
                res2 = req['request']['original_utterance'][mid:end]
                res3 = req['request']['original_utterance'].lower()[-8:]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                res3 = [i for i in res3.split() if i.isdigit()]
                res3 = ''.join(res3)
                res3 = int(res3)
                if res3 >= 0 and res3 <=255:
                    if res1 >= 1 and res1 <= len(User_s[user_id])+1:
                        if res2 >=0 and res2 <=len(User_ch[user_id]):
                            print(User_s[user_id][res1-1]+res2-1, res3)
                            print(User_s[user_id][res1-1]+res2-1, res3)
                            User_dev[user_id].send_single_value(User_s[user_id][res1-1]+res2-1, res3)
                            res['response']['text'] = 'Сигнал отправлен'
                            res['response']['buttons'] = get_suggests(1)
                            return
                        else:
                            res['response']['text'] = 'Канал не найден'
                            res['response']['buttons'] = get_suggests(1)
                            return
                    else:
                        res['response']['text'] = "Устройство не найдено"
                        res['response']['buttons'] = get_suggests(1)
                        return
                else:
                    res['response']['text'] = "Некорректное значение"
                    res['response']['buttons'] = get_suggests(1)
                    return
        elif req['request']['original_utterance'].lower().find("закончить")>=0:
            UserInfo[user_id]=0
            res['response']['text'] = "Заканчиваю работу мастер-контроль"
            res['response']['buttons'] = get_suggests(1)
            User_dev[user_id].close()
            return
        else:
            res['response']['text'] = "Команда не опознана"
            res['response']['buttons'] = get_suggests(1)
            return
if __name__ == '__main__':
    app.run()