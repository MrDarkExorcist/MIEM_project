def find_ch(n, ch, str):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d_ch_%d" % (n,ch))
    line = f.readline()
    s=-1
    count=0
    subcount=-1
    while line:
        count+=1
        if count==4:
            start=int(line)
        if count>4:
            subcount+=1
            if line==str:
                s=int(count+start-5-subcount/2)
                break
        line = f.readline()
    return(s)

def find_ch_n(n, ch, d):
    f=open("/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d_ch_%d" % (n,ch))
    line = f.readline()
    s=-1
    count=0
    subcount=-1
    while line:
        count+=1
        if count==4:
            start=int(line)
        if count>4:
            subcount+=1
            if int(subcount/2)==d-1:
                s=int(count+start-5-subcount/2)
                break
        line = f.readline()
    return(s)
        
print(find_ch(1,2,"Диммер\n"))
print(find_ch(1,2,"Стробы\n"))
print(find_ch(2,8,"Диммер\n"))
print(find_ch(2,8,"Стробы\n"))
print(find_ch(3,15,"Диммер\n"))
print(find_ch(3,15,"Стробы\n"))
print(find_ch_n(1,2,1))
print(find_ch_n(1,2,2))
print(find_ch_n(2,8,4))
print(find_ch_n(2,8,5))