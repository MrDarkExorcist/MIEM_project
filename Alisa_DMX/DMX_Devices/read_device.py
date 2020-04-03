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
    
print(numify("<n>=(ноль | один | два | три | четыре | пять | шесть | семь | восемь | девять );"))