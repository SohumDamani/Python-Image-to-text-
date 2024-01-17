import os
import re
import easyocr
from matplotlib import pyplot as plt
import datetime
from PIL import ImageGrab
import emoji
import time


def convert_to_readable(min):
    temp = str(datetime.timedelta(minutes=min))
    return temp.split(' ')[-1]

def update_arr(arr,idx):
    to_update = input((f" Do you want to update {arr[idx]} ? (y/n) : ")) 
    if to_update == "y":
        new_value = input("Enter new value with AM and PM : ")
        arr[idx] = new_value
    return arr

def read_snapshot():
    
    attempt = 0
    while True:
        attempt+=1
        im = ImageGrab.grabclipboard()
        if not im:
            print(emoji.emojize("Snapshot toh lele :face_with_raised_eyebrow:"))
            if attempt==5:
                print("Your attempts are over .")
                exit()
            time.sleep(5)
        else:
            print("Extracting data from the image .......")
            im.save('test.png','PNG')
            return
        
def extract_data(andar,bahar):
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
# Autosave image after snipping


while True:
    read_snapshot()
    IMAGE_PATH = "test.png"
    reader = easyocr.Reader(['en'])
    result = reader.readtext(IMAGE_PATH,paragraph="False")
    req = list(map(lambda x: result[x][-1],range(len(result))))

    #print(result)
    #print(req)
    andar = []
    bahar = []

    extract_data(andar,bahar)
    print("Your swipe In timings : ",andar)
    print("Your swipe Out timings : ",bahar)

    check = input("Does your timings match ? (y/n) :")
    if check=='n':
        print("Image coludn't be read properly. Use the following options : \
                        \n 1. To edit timing manually \
                        \n 2. To retake screenshot \
                        \n 3. To exit")
        flag = int(input("Choose your option wisely : "))

        if flag==1:
            while True:
                attempt = 0
                while attempt<=2:
                    arr = int(input("Which do you want to edit : \n1. In \n 2.Out \n3.Exit"))
                    if arr in [1,2,3]:
                        break
                    else:
                        print(f"{2-attempt} attempt left")
                    attempt+=1

                    if attempt==3:
                        print("Lost all your chances")
                        exit
                if arr ==3:
                    break
                idx = int(input("Enter index to be updated : "))
                if arr == 1:
                    update_arr(andar,idx)
                elif arr == 2:
                    update_arr(bahar,idx)
                else:
                    break

                print(f" Updated timings \nYour swipe In timings : {andar} \nYour swipe Out timings : {bahar}")
        elif flag == 2:
            pass
    andar_min = []
    bahar_min = []

    for i in andar:
        temp = re.split(r'\s|\.|\:',i)
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
        
    hours_to_be_in_office = int(input(emoji.emojize("Kitni der karna hai office me :eyes:   ")))

    print( emoji.emojize("Extra time hai tere pass? :smirking_face:"))
    extra_time = int(input("Kam zyada jo ho imadari se daal  : "))

    min_left = (hours_to_be_in_office)*60-in_time-extra_time

    # print(f"Leave left : {min_left}")
    # print(f"Inside {andar_min[-1]}")

    print(f"Leave at : {convert_to_readable(andar_min[-1]+min_left)}")

    os.remove("test.png")
    exit()
        
           
                    





