import sensor,image,time,math
from pyb import LED,UART
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False,200)
sensor.set_auto_whitebal(False)
sensor.skip_frames(20)
clock = time.clock()
thresholds=(60,255)
uart1=UART(1,19200)
uart=UART(3,115200)
sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0).save("bg.bmp")
while(True):
    max_s=0
    com=uart.readline()
    if(com):
        com=com.decode()
        uart1.write(com)
    mes=uart1.readline()
    if(mes):
        mes=mes.decode()
        uart.write(mes)
        continue
    mes=uart1.readline()
    img=sensor.snapshot().lens_corr(strength =1.7, zoom = 1.0).save("bg1.bmp")
    img1=image.Image("bg.bmp")
    img.difference(img1)
    img.binary([thresholds])
    image.Image("bg1.bmp").save("bg.bmp")
    white=(1,255)
    blobs=img.find_blobs([white],x_stride=5,y_stride=1,area_threshold=10,pixels_threshold=10)
    for blob in blobs:
        if(blob.area()>max_s):
            max_s=blob.area()
            blob_m=blob
    if(blobs):
        if(blob_m.cx()>80):
            uart.write(chr(5))
            uart.write(chr(blob_m.cx()-80))
        else:
            uart.write(chr(4))
            uart.write(chr(80-blob_m.cx()))
