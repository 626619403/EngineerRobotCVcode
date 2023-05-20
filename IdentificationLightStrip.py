import sensor,image,time,math
from pyb import LED,UART
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False,2000)
sensor.set_auto_whitebal(False)
thresholds=(50,255)
uart1=UART(1,19200)
uart=UART(3,115200)
led=LED(2)
led.on()
tag=1
num=0
while(True):
    max_s=0
    num+=1
    com=uart.read(1)
    if(com):
        print(com)
        try:
            com=com.decode('UTF-8','ignore')
        except:
            pass
        uart1.write(com)
    mes=uart1.read(2)
    if(mes):
        num=0
        print(mes)
        try:
            mes=mes.decode('UTF-8','ignore')
        except:
            pass
        if(mes[0]==chr(4)):
            flag=0
            if(tag==1):
                sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0).save("bg.bmp")
                tag=0
            img=sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0).save("bg1.bmp")
            img1=image.Image("bg.bmp")
            img.difference(img1)
            img.binary([thresholds])
            image.Image("bg1.bmp").save("bg.bmp")
            white=(1,255)
            blobs=img.find_blobs([white],x_stride=5,y_stride=1)
            for blob in blobs:
                if(blob.area()>max_s and blob.w()>blob.h()):
                    max_s=blob.area()
                    blob_m=blob
                    flag=1
            if(flag==1):
                img.draw_rectangle(blob_m.rect())
                if(blob_m.cx()>80):
                    uart.write('%c%c'%(chr(5),chr(blob_m.cx()-80)))
                else:
                    uart.write('%c%c'%(chr(4),chr(80-blob_m.cx())))
                print(blob_m.cx())
            else:
                uart.write('%c%c'%(chr(6),chr(0)))
        else:
            uart.write(mes)
    if(num>200000):
        num=0
        print(1000)
        for i in range(100):
            uart.write('%c%c'%(chr(0),chr(1)))
