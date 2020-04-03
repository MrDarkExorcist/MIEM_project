#! /usr/bin/env python
#-*- coding: utf-8 -*-
#project: home-smart-home.ru
import subprocess
import time
from datetime import date
import os.path
from pyudmx import pyudmx
import json
import logging

l_ch = []
l_val = []
l_s = []

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

def numify(str):
    str=str.replace("ноль","0")
    str=str.replace("один","1")
    str=str.replace("два","2")
    str=str.replace("три","3")
    str=str.replace("четыре","4")
    str=str.replace("пять","5")
    str=str.replace("шесть","6")
    str=str.replace("восемь","8")
    str=str.replace("семь","7")
    str=str.replace("девять","9")
    return(str)

def describe(n):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (n))
    line = f.readline()
    count = 0
    while count<=4:
        count+=1
        if count==1:
            print("Номер девайса:",line[:-1])
            line = f.readline()
            continue
        if count==2:
            print("Название:",line[:-1])
            line = f.readline()
            continue
        if count==3:
            print("Каналы:",line[:-1])
            line = f.readline()
            continue
        if count==4:
            print("Стартовый канал:",line[:-1])
            line = f.readline()
            continue
    f.close()
    return

def read_device(n):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (n))
    line = f.readline()
    s=0
    count=0
    while line:
        count+=1
        if count==1:
            print("Номер девайса:",line[:-1])
            line = f.readline()
            continue
        if count==2:
            print("Название:",line[:-1])
            line = f.readline()
            continue
        if count==3:
            print("Каналы:",line[:-1])
            ch=int(line)
            line = f.readline()
            continue
        if count==4:
            print("Стартовый канал:",line[:-1])
            sch=int(line)
            line = f.readline()
            s=1
            continue
        if count>(4+ch+ch):
            break
        if count%2==1:
            lined = f.readline()
            print(s,"канал:",line[:-1],'|',lined[:-1])
            line = f.readline()
            count+=1
            s+=1
            continue
    f.close()
    
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
                    print(line)
                    fl=False
                    break
            line = f.readline()
        if fl:
            print("Канал не найден")
        f.close()
        return

def device_load(number, channels):
    subprocess.call("rm 'device_%d'" % (number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("cp 'device_%d_ch_%d' '/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d'" % (number, channels, number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    return

exe = '''pocketsphinx_continuous -adcdev plughw:0,0 -hmm /home/pi/zero_ru_cont_8k_v3/zero_ru.cd_semi_4000/ -jsgf /home/pi/Alisa_DMX/gram_rus.gram -dict /home/pi/Alisa_DMX/vocab_ready -inmic yes'''
p = subprocess.Popen(["%s" % exe], shell=True, stdout=subprocess.PIPE)
 
while True:
        retcode = p.returncode 
        line = p.stdout.readline()
        line = line.decode('utf-8')
        line=numify(line[11:])
        if line == "Димакс журнал\n":
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/log.txt","r")
            print(f.read())
            f.close()
        elif line == "Димакс журнал очисти\n":
            print(line)
            subprocess.call("rm '/home/pi/Alisa_DMX/DMX_Devices/Config/log.txt'", shell=True)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/log.txt","r")
            print(f.read())
            f.close()
        elif line == "Димакс конфигурация загрузи\n":
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')    
            num=0
            while os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d" % (num+1)):
                num+=1
            for j in range(num):
                s, val=scan(j+1)
                l_s.append(s)
                l_val.append(s)
                l_ch.append(len(val))
            print("Загружено устройств: %d" % (int(num+1)))
            DMX = pyudmx.uDMXDevice()
            DMX.open()
            d=0
            for i in l_s:
                '''count=0
                for j in l_val:
                    DMX.send_single_value(count+i, j)
                    count+=1'''
                d+=1
                print("Прибор %d готов" % d)
            print("Конфигурация завершена")
        elif line == "Димакс конфигурация обнови\n":
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            for i in range(len(l_s)):
                device_dump(i+1, len(l_val), l_val, l_s[i])
                print("Прибор %d обновлен:" % i)
        elif line == "Димакс прибор список\n":
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            for i in range(len(l_s)):
                describe(i+1)
        elif line == "Димакс прибор проверка\n":
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            check=0
            flag=False
            for i in range(len(l_s)-1):
                check+=l_ch[i]+l_s[i]
                if l_s[i+1]<check:
                    print("Конфликт приборов %d %d" % (i+1, i+2))
                    flag=True
                check=0
            if flag:
                print("Переобозначьте стартовые каналы!")
                for i in range(len(l_s)):
                    print("Прибор %d:" % i+1)
                    l_s[i]=int(input())
            else:
                print("Конфликтов не обнаружено.")
        elif line.find("все каналы")>=0:
            if line.find("сброс")>=0:
                print(line)
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                res = [i for i in line.split() if i.isdigit()]
                res = ''.join(res)
                res = int(res)
                if res >= 1 and res <= len(l_s)+1:
                    s, val=scan(res)
                    l_val[res-1]=val
                    print("Каналы сброшены")
                else:
                    print("Устройство не найдено")
            elif line.find("смени")>=0:
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = line.find("прибор")
                mid = line.find("канал")
                res1 = line[beg:mid]
                res2 = line[-8:]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                if res >= 1 and res <= len(l_s)+1:
                    if os.path.exists("/home/pi/Alisa_DMX/DMX_Devices/Config/var/device_%d_ch_%d" % (res1,res2)):
                        device_load(res1,res2)
                        s, val=scan(res1)
                        l_s[res1-1]=s
                        l_val[res1-1]=val
                        l_ch[res1-1]=res2
                    print("Набор каналов изменен")
                else:
                    print("Устройство не найдено")
        elif line.find("стартовый канал")>=0:
            if line.find("инфо")>=0:
                print(line)
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                res = [i for i in line.split() if i.isdigit()]
                res = ''.join(res)
                res = int(res)
                if res >= 1 and res <= len(l_s)+1:
                    answer, buf=scan(res)
                    print("Стартовый канал прибора %d: %d" % (res, answer))
                else:
                    print("Устройство не найдено")
            elif line.find("отправь")>=0:
                print(line)
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = line.find("прибор")
                mid = line.find("канал")
                res1 = line[beg:mid]
                res2 = line[-8:]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                if res1 >= 1 and res1 <= len(l_s)+1:
                    l_ch[res1-1]=res2
                    print("Стартовый канал сменен")
                else:
                    print("Устройство не найдено")
        elif line.find("канал")>=0:
            if line.find("инфо")>=0:
                print(line)
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                beg = line.find("прибор")
                mid = line.find("канал")
                end = line.find("инфо")
                res1 = line[beg:mid]
                res2 = line[mid:end]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                if res1 >= 1 and res1 <= len(l_s)+1 and res2 >=1:
                    find_ch_n(res1,res2)
                else:
                    print("Канал или устройство не найдены")
            elif line.find("отправь")>=0:
                subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
                res = [i for i in line.split() if i.isdigit()]
                beg = line.find("прибор")
                mid = line.find("канал")
                end = line.find("отправь")
                res1 = line[beg:mid]
                res2 = line[mid:end]
                res3 = line[-8:]
                res1 = [i for i in res1.split() if i.isdigit()]
                res1 = ''.join(res1)
                res1 = int(res1)
                res2 = [i for i in res2.split() if i.isdigit()]
                res2 = ''.join(res2)
                res2 = int(res2)
                res3 = [i for i in res3.split() if i.isdigit()]
                res3 = ''.join(res3)
                res3 = int(res3)
                print(res1,res2,res3)
                if res3 >= 0 and res3 <=255:
                    if res1 >= 1 and res1 <= len(l_s)+1:
                        if res2 >=0 and res2 <=len(l_ch):
                            DMX.send_single_value(l_s[res1-1]+res2-1, res3)
                            #l_val[res-1][res2]=res3
                        else:
                            print("Канал не найден")
                    else:
                        print("Устройство не найдено")
                else:
                    print("Некорректное значение")
                            
        elif line.find("конфигурация")>=0 and line.find("прибор")>=0:
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            res = [i for i in line.split() if i.isdigit()]
            res = ''.join(res)
            res = int(res)
            if res >= 1 and res <= len(l_s)+1:
                device_dump(res, l_ch[res-1], l_val[res-1], l_s[res-1])
                print("Конфигурация устройства обновлена")
            else:
                print("Устройство не найдено")
        elif line.find("сброс")>=0:
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            res = [i for i in line.split() if i.isdigit()]
            res = ''.join(res)
            res = int(res)
            if res >= 1 and res <= len(l_s)+1:
                s, val=scan(res)
                l_s[res-1]=s
                l_ch[res-1]=len(val)
                l_val[res-1]=val
                count=0
                for j in val:
                    DMX.send_single_value(l_s[res-1]+count, j)
                    count+=1
                print("Устройство сброшено до конфигурации")
            else:
                print("Устройство не найдено")
        elif line.find("инфо")>=0:
            print(line)
            subprocess.call("echo '%s %s %s' >> 'log.txt'" % (time.strftime("%H:%M:%S"),date.today(),line[:-1]), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
            res = [i for i in line.split() if i.isdigit()]
            res = ''.join(res)
            res = int(res)
            if res >= 1 and res <= len(l_s)+1:
                read_device(res)
            else:
                print("Устройство не найдено")   
        else:
            print(line)
            time.sleep(0.15)
        if(retcode is not None):
                DMX.close()                                                                                                                                                                                                  
                break