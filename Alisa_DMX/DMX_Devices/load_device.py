def device_load(number, device, channels):
    subprocess.call("rm 'device_%d'" % (number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config')
    subprocess.call("cp 'device_%d_ch_%d' '/home/pi/Alisa_DMX/DMX_Devices/Config/device_%d'" % (device, channels, number), shell=True,cwd='/home/pi/Alisa_DMX/DMX_Devices/Config/var')
    return