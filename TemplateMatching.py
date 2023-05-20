import sensor,image,time,json,math
from image import SEARCH_EX, SEARCH_DS
from pyb import UART,LED
uart=UART(3,19200)
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
st=".pgm"
led=LED(3)
led.on()
x_d=80
flag=0
while(True):
    img = sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0)
    jud=uart.read(1)
    if(jud):
        jud=jud.decode()
        if(jud==chr(0)):
            flag=0
        elif(jud==chr(1)):
            flag=1
            x_d=80
        elif(jud==chr(2)):
            flag=2
    else:
        if(flag==0):
            continue
    if(flag==2):
        sensor.set_framesize(sensor.QQQVGA)
        for i in range(7):
            r = img.find_template(image.Image('/'+str(i)+st),0.7,step=4,search=SEARCH_EX)
            if r:
                uart.write(chr(3)+chr(i))
                break
    elif(flag==1):
        for i in range(7):
            sensor.set_framesize(sensor.QQVGA)
            r = img.find_template(image.Image('/1'+str(i)+st),0.7,step=4,search=SEARCH_EX)
            if r:
                if(abs(abs(r[0]+r[2]/2-80)-x_d)>40):
                    continue
                if(r[0]+r[2]/2>80):
                    uart.write(chr(2)+chr(r[0]+r[2]/2-80))
                else:
                    uart.write(chr(1)+chr(80-r[0]-r[2]/2))
                x_d=abs(r[0]+r[2]/2-80)
                break
