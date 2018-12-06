# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2 as cv
import time
from PIL import Image, ImageFont, ImageDraw
import matplotlib as plt
def get_text_dic(text):
    text_dic={}
    im = Image.new("RGB", (40, 40), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "simhei.ttf"), 28)
    dr.text((10, 5), text, font=font, fill="#000000")
    a=np.array(im)[:,:,0].mean()
    Max=0
    Min=255
    for i in text:
        im = Image.new("RGB", (40, 40), (255, 255, 255))
        dr = ImageDraw.Draw(im)
        dr.text((10, 5), i, font=font, fill="#000000")
        Mean=np.array(im)[:,:,0].mean()
        text_dic[i]=Mean
        if Mean>Max:
            Max=Mean
        if Mean<Min:
            Min=Mean
    for i in text_dic.keys():
        text_dic[i]=(text_dic[i]-Min)/(Max-Min)*255 #归一化
    return text_dic

source_image_path='a.jpg'
text = "床前明月光，疑是地上霜。举头望明月，低头思故乡 从前有座山 山上有座庙 庙里有个老和尚 苟利国家生死以岂因祸福避趋之"
img_dir="./pic_res"
text_resolution=100
re=""
dic=get_text_dic(text)
l=[" " for i in range(256)]
min_err=1000
min_key=""
for ll in range(256):
    for key in dic.keys():
        err=abs(dic[key]-ll)
        if err<min_err:
            min_err=err
            min_key=key
    l[ll]=min_key
    min_err=1000
def draw(img):
    re=""
    source_im= Image.fromarray(cv.cvtColor(img,cv.COLOR_BGR2RGB)) 
    im1 = source_im.convert('L') 
    x=text_resolution
    im1 = np.array(im1.resize((x, int(x*3/4))))
    for i in np.array(im1):
        for j in i:
            re+=l[j]
        re+="\r\n"
#with open("re.txt","w") as f:
#        f.write(re)
    #time.sleep(1/30)
    os.system('cls')       
    print("\n"+re)     

cap=cv.VideoCapture('test.mp4')
frame_count = 1
success = True
success, frame = cap.read()
while(success):
    success, frame = cap.read()
    if success:
        draw(frame) 
    frame_count = frame_count + 1
cap.release()