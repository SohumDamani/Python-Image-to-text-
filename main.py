import os
import re
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import datetime
from PIL import ImageGrab
import emoji


def convert_to_readable(min):
    return datetime.timedelta(minutes= min)

# Autosave image after snipping

while True:

    im = ImageGrab.grabclipboard()

    if not im:
        print(emoji.emojize("Snapshot toh lele :face_with_raised_eyebrow:"))
    else:
        im.save('test.png','PNG')
        IMAGE_PATH = "test.png"
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH,paragraph="False")
        req = list(map(lambda x: result[x][-1],range(len(result))))

        # print(result)
        print(req)
        andar = []
        bahar = []

        cnt = 0
        for idx,i in enumerate(req):
            if ("AM" in i or "PM" in i):
                if cnt%2==0:
                    andar.append(i)
                    cnt+=1
                else:
                    bahar.append(i)
                    cnt+=1
    
        if len(andar)==0 or len(bahar)==0:
            print(emoji.emojize("Snapshot dhang se le be :unamused_face:"))
            exit()
        print("Your swipe In timings : ",andar)
        print("Your swipe Out timings : ",bahar)

        check = input("Does your timings match ? (y/n) :")
        if check=='y':
            andar_min = []
            bahar_min = []

            for i in andar:
                temp = re.split(r'\s|\.',i)
                if temp[-1]=="AM":
                    x = int(temp[0])*60+int(temp[1])
                else:
                    x = (int(temp[0])+12)*60+int(temp[1])
                
                andar_min.append(int(x))


            for i in bahar:
                temp = re.split(r'\s|\.|:',i)
                if temp[-1]=="AM":
                    x = int(temp[0])*60+int(temp[1])
                else:
                    x = (int(temp[0])+12)*60+int(temp[1])
                bahar_min.append(int(x))

            out = 0
            for i in range(len(bahar_min)):
                out += andar_min[i+1]-bahar_min[i]

            in_time = 0
            for i in range(len(bahar_min)):
                in_time += bahar_min[i]-andar_min[i]
            # print("Mintues out :",out)
            # print("Minutes inside : ",in_time)

            print( emoji.emojize("Extra time hai tere pass? :smirking_face:"))
            extra_time = int(input("Kam zyada jo ho imadari se daal  : "))

            min_left = 8*60-in_time-extra_time

            # print(f"Leave left : {min_left}")

            print(f"Leave at : {convert_to_readable(andar_min[-1]+min_left)}")

            os.remove("test.png")
            exit()
        else:
            flag = input("Image coludn't be read properly.Retake the snapshot and enter yes : ")
            


