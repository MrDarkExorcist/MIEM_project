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

describe(1)