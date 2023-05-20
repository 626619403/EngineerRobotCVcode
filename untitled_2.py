import sensor,image,time,json,math,pyb
from pyb import UART,LED
uart=UART(3,19200)
sensor.reset()
sensor.set_contrast(-2)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_auto_exposure(False,200000)
#sensor.set_auto_whitebal(False)
st=".bmp"
led=LED(2)
led.on()
time_start = pyb.millis()
try:
    fil=open('pho.txt','a+')
finally:
    if(fil):
        s=fil.readline()
    #while():
    time.sleep_ms(100)
    duration=pyb.elapsed_millis(time_start)
    print(duration)

