import subprocess
class Device:
    
    def __init__(self, number, name, channels, start_channel, channel_name, channel_value):
        self.number=int(number)
        self.name=name
        self.channels=int(channels)
        self.start_channel=int(start_channel)
        self.channel_name=channel_name
        self.channel_value=channel_value
    def __del__(self):
        print(self.name, "Устройство удалено.")
    def display_info(self):
        print("Номер устройства:",self.number)
        print("Название устройства:",self.name)
        print("Количество каналов:",self.channels)
        print("Номер начального канала:",self.start_channel)
        print("Имена каналов:",self.channel_name)
        print("Значения каналов:",self.channel_value)
        
def device_create():
    print("Добро пожаловать в конструктор прибора!")
    print("Введите номер устройства:")
    n=int(input())
    print("Введите название устройства:")
    name=input()
    print("Введите количество каналов устройства:")
    number=int(input())
    print("Введите начальный канал устройства:")
    start=int(input())
    print("Введите имена каналов устройства:")
    list1=[]
    for i in range(number):
        list1.append(input())
    print("Выставить нулевые значения? y/n")
    while True:
        choice=input()
        if choice=='y':
            list2=[0]*number
            break
        if choice=='n':
            print("Введите значения каждого канала, значения от 0 до 255")
            list2=[]
            for i in range(number):
                print(list1[i])
                while True:
                    d=int(input())
                    if d>=0 and d<=255:
                        list2.append(d)
                        break
                    else:
                        print("Неккоректное значение. Давайте еще раз.")
            break
        print("Неккоректное значение. Давайте еще раз.")   
    namefile='device_%d_ch_%d' % (n,number)
    subprocess.call("rm '%s'" % (namefile), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("echo '%d' >> '%s'" % (n,namefile), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("echo '%s' >> '%s'" % (name, namefile),shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("echo '%d' >> '%s'" % (number, namefile),shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("echo '%d' >> '%s'" % (start, namefile),shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    for i in range(number):
        subprocess.call("echo '%s' >> '%s'" % (list1[i], namefile),shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
        subprocess.call("echo '%d' >> '%s'" % (list2[i], namefile),shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    return

def device_dump(number, channels, value):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d_ch_%d" % (number, channels))
    namefile='device_%d_ch_%d_new' % (number, channels)
    for i in range(4):
        line = f.readline()
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    for i in range(channels):
        line = f.readline()
        subprocess.call("echo '%s' >> '%s'" % (line[:-1],namefile), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
        line = f.readline()
        subprocess.call("echo '%d' >> '%s'" % (value[i],namefile), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("rm 'device_%d_ch_%d'" % (number, channels), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("mv '%s' 'device_%d_ch_%d'" % (namefile, number, channels), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    return
device_dump(2, 4, [1,1,1,1])
