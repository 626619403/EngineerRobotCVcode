import sensor,image,time,json,math,pyb
from image import SEARCH_EX, SEARCH_DS
from pyb import UART,LED
uart=UART(3,19200)
sensor.reset()
sensor.set_contrast(-2)
sensor.set_gainceiling(16)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
#sensor.set_auto_exposure(False,200000)
#sensor.set_auto_whitebal(False)
st=".pgm"
led=LED(2)
led.on()
flag=0
x_d=80
time_start = pyb.millis()
yellow=(24, 80, -18, 41, 30, 62)
while(True):
    jud=uart.read(1)
    if(jud):
        try:
            jud=jud.decode()
            if(jud==chr(0)):
                flag=0
            elif(jud==chr(1)):
                flag=1
                x_d=80
            elif(jud==chr(2)):
                flag=2
            elif(jud==chr(3)):
                duration=pyb.elapsed_millis(time_start)
                sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0).save('/'+str(duration)+'bmp')
            elif(jud==chr(4)):
                flag=4
                x_d=80
                sensor.set_contrast(1)
                sensor.set_gainceiling(16)
        except:
            pass
    #flag=1
    k=1
    if(flag==0):
        uart.write('%c%c'%(chr(7),chr(0)))
    if(flag==2):
        sensor.set_pixformat(sensor.GRAYSCALE)
        img = sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0)
        for i in range(8):
            r = img.find_template(image.Image('/'+str(i)+st),0.7,step=4,search=SEARCH_EX)
            if r:
                k=0
                img.draw_rectangle(r)
                uart.write('%c%c'%(chr(3),chr(i)))
                break
        if(k==1):
            uart.write('%c%c'%(chr(8),chr(0)))
    elif(flag==1):
        sensor.set_pixformat(sensor.RGB565)
        img = sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0)
        min_x=100
        dire='0'
        blobs=img.find_blobs([yellow],pixels_threshold=100,margin=2)
        lis=[0,0,0,0]
        for blob in blobs:
            k=0
            d=blob.cx()-80
            if(abs(d-x_d)>30):
                x_d=d
                continue
            if(abs(d)<min_x):
                min_x=abs(d)
                lis=blob.rect()
                if(d<0):
                    dire=chr(1)
                else:
                    dire=chr(2)
        img.draw_rectangle(lis)
        uart.write('%c%c'%(dire,chr(min_x)))
        if(k==1):
            uart.write('%c%c'%(chr(4),chr(0)))
    elif(flag==4):
        min_x=100
        sensor.set_pixformat(sensor.GRAYSCALE)
        time.sleep_ms(200)
        img = sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0)
        for i in range(1,5):
            r = img.find_template(image.Image('/1'+str(i)+st),0.7,step=4,search=SEARCH_EX)
            if r:
                sta=img.get_statistics(roi=r)
                if(sta.mean()<20 or sta.mean()>90):
                    pass
                else:
                    img.draw_rectangle(r)
                    k=0
                    if(abs(r[0]+r[2]//2-80-x_d)>30):
                        x_d=r[0]+r[2]//2-80
                        continue
                    x_d=r[0]+r[2]//2-80
                    if(r[0]+r[2]//2>80):
                        uart.write('%c%c'%(chr(2),chr(abs(x_d))))
                    else:
                        uart.write('%c%c'%(chr(1),chr(abs(x_d))))
                    break
        if(k==1):
            uart.write('%c%c'%(chr(4),chr(0)))
