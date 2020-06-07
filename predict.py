import tensorflow as tf
import numpy as np
from os import listdir
from os.path import isfile, join
import cv2
import os

def iss(a,b):
    if(a[0]!=b[0]):
        return 0
    if(a[1]!=b[1]):
        return 0
    if(a[2]!=b[2]):
        return 0
    return 1

inp = str(raw_input('The name of the folder containing images for testing: '))

onlyfiles = [f for f in listdir(inp) if isfile(join(inp, f))]
fin = np.empty((4*len(onlyfiles),64,32,3))
m = 0
l = []
for index in range(len(onlyfiles)):
    img = cv2.imread(inp + "/" +  onlyfiles[index],1)
    pi = img[0,0]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]-10,img.shape[1]):
            img[i,j] = pi
    for i in range(img.shape[0]):
        for j in range(0,10):
            img[i,j] = pi
    for j in range(img.shape[1]):
        for i in range(img.shape[0]-10,img.shape[0]):
            img[i,j] = pi
    for j in range(img.shape[1]):
        for i in range(0,10):
            img[i,j] = pi
    for j in range(img.shape[1]):
        flag1 =0
        ras = 0
        for i in range(img.shape[0]):
            if flag1==0 and iss(img[i,j],pi):
                continue
            if flag1==0 and (not iss(img[i,j],pi)):
                flag1=1
                ras = i
                continue
            if flag1==1 and (not iss(img[i,j],pi)):
                continue
            if flag1==1 and iss(img[i,j],pi):
                if i-ras<20:
                    for k in range(ras,i+1):
                        img[k,j]=pi
                flag1=0
    for i in range(img.shape[0]):
        flag1 =0
        ras = 0
        for j in range(img.shape[1]):
            if flag1==0 and iss(img[i,j],pi):
                continue
            if flag1==0 and (not iss(img[i,j],pi)):
                flag1=1
                ras = j
                continue
            if flag1==1 and (not iss(img[i,j],pi)):
                continue
            if flag1==1 and iss(img[i,j],pi):
                if j-ras<20:
                    for k in range(ras,j+1):
                        img[i,k]=pi
                flag1=0
    start = []
    end = []
    flag = 0
    for j in range(img.shape[1]):
        flag2 = 0
        for i in range(img.shape[0]):
            if flag2 == 0 and not iss(img[i,j],pi):
                flag2 = 1
            if flag == 0 and not iss(img[i,j],pi):
                start.append(j-5)
                flag = 1
            if flag == 1 and i==img.shape[0]-1 and flag2==0:
                flag = 0
                end.append(j+5)
    if(len(start)>len(end)):
        start.remove(start[len(start)-1])
    if start[0]<10:
        start.remove(start[0])
        end.remove(end[0])
    for i in range(len(start)):
        flagn = 1
        if i == len(start):
            break
        for a in range(0+10,img.shape[0]-10):
            for b in range(start[i]+10,end[i]-10):
                if not iss(img[a,b],pi):
                    flagn =0
        if flagn==1:
            start.remove(start[i])
            end.remove(end[i])
            i=i-1
    for i in range(len(start)):
        if i == len(start):
            break
        if end[i]-start[i]<10:
            start.remove(start[i])
            end.remove(end[i])
            i = i-1
    l.append(len(start))
    for i in range(len(start)):
        img1 = img[:,start[i]:end[i]]
        arr = np.array(img1)
        arr1 = cv2.resize(arr,(32,64))
        fin[m] = arr1
        m = m+1

model = tf.keras.models.load_model('my_model.h5')
start = 0
end = l[0]
for index in range(len(l)):
    y_pred = model.predict(fin[start:end])
    y  = []
    for i in y_pred:
        for j in range(len(i)):
            if i[j]==1:
                y.append(j + ord('A'))
                break
    ans = ''
    for i in range(len(y)):
        ans = ans+(chr(y[i]))
    img = cv2.imread(inp + "/" +  onlyfiles[index],1)
    cv2.imshow(ans, img)
    if index!= len(l)-1:
        start = end
        end = end + l[index+1]
cv2.waitKey(0)
