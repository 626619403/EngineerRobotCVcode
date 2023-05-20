import sensor,image,time,json,math
from image import SEARCH_EX, SEARCH_DS
from pyb import UART,LED
uart=UART(3,19200)
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
st=".pgm"
led=LED(2)
led.on()
flag=0
while(True):
    img = sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0)
    try:
        jud=uart.read(1)
    except:
        print(3)
    if(jud):
        print(jud)
        try:
            jud=jud.decode()
        except:
            print(3)
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
    k=1
    if(flag==2):
        for i in range(8):
            r = img.find_template(image.Image('/'+str(i)+st),0.7,step=4,search=SEARCH_EX)
            if r:
                k=0
                img.draw_rectangle(r)
                uart.write('%c%c'%(chr(3),chr(i)))
                break
        if(k==1):
            uart.write('%c%c'%(chr(4),chr(0)))
    elif(flag==1):
        for i in range(1,4):
            r = img.find_template(image.Image('/1'+str(i)+st),0.8,step=4,search=SEARCH_EX)
            if r:
                sta=img.get_statistics(roi=r)
                if(sta.mean()<=5):
                    continue
                k=0
                x_d=r[0]+r[2]//2
                if(abs(r[0]+r[2]//2-x_d)>30):
                    continue
                img.draw_rectangle(r)
                if(r[0]+r[2]//2>80):
                    uart.write('%c%c'%(chr(2),chr(r[0]+r[2]//2-80)))
                else:
                    uart.write('%c%c'%(chr(1),chr(80-r[0]-r[2]//2)))
                break
        if(k==1):
            uart.write('%c%c'%(chr(4),chr(0)))
