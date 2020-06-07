from os import listdir
from os.path import isfile, join
import cv2
import numpy as np

def iss(a,b):
    if(a[0]!=b[0]):
        return 0
    if(a[1]!=b[1]):
        return 0
    if(a[2]!=b[2]):
        return 0
    return 1


onlyfiles = [f for f in listdir('train') if isfile(join('train', f))]
#print(onlyfiles)
names = []

for i in onlyfiles:
    temp = ""
    for j in i:
        if j is ".":
            names.append(temp)
            break
        temp = temp + j
max1 = 0
min1 = 100000
for index in range(len(onlyfiles)):
    img = cv2.imread("train/" +  onlyfiles[index],1)
    cv2.imshow('image12',img)
    pi = img[0,0]
    print(iss(img[67,54],pi))
    print(pi)
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
    cv2.imshow('img1',img)


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
    cv2.imshow('imgn',img)


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


    print(start)
    print(end)
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
    name = names[index]
    print(name)
    print(start)
    print(end)
    for i in range(len(start)):
        min1 = min(min1,end[i]-start[i])
        max1 = max(max1,end[i]-start[i])
    for i in range(len(start)):
        img1 = img[:,start[i]:end[i]]
        arr = np.array(img1)
        arr1 = cv2.resize(arr,(32,64))
        cv2.imwrite('preprocessed/'+name[i] + str(index)+'.png',arr1)
        #cv2.imshow('image' + str(i),arr1)


    #cv2.waitKey(0)
print(min1)
print(max1)
