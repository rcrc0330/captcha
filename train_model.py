import tensorflow as tf
import numpy as np
from os import listdir
from os.path import isfile, join
import cv2

onlyfiles = [f for f in listdir('preprocessed') if isfile(join('preprocessed', f))]
names = []

for i in onlyfiles:
    names.append(i[0])
img =[]

for index in range(len(onlyfiles)):
    img.append(cv2.imread("preprocessed/" +  onlyfiles[index],1))

arr = np.empty((len(img),img[0].shape[0],img[0].shape[1],img[0].shape[2]))
arr1 = np.empty((len(img),img[0].shape[0],img[0].shape[1],img[0].shape[2]))
for i in range(len(img)):
    arr[i] = np.array(img[i])
    arr1[i] = cv2.resize(arr[i],(img[0].shape[1],img[0].shape[0]))

arr2 = np.empty(len(names))
for i in range(len(names)):
    arr2[i] = ord(names[i])-ord('A')
training_images = arr1[0:6000]
training_labels = arr2[0:6000]
test_images = arr1[6000:len(arr1)]
test_labels = arr2[6000:len(arr2)]
training_images=training_images/255.0
test_images=test_images/255.0
print(training_labels[1])
print(names[1])
cv2.imshow('img1',training_images[1])

#training_images = training_images/255.0
#test_images = test_images/255.0
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(img[0].shape[0],img[0].shape[1],img[0].shape[2])),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(26, activation='softmax')
])

model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images,training_labels,epochs = 5)



test_loss = model.evaluate(test_images, test_labels)
model.save('my_model.h5')
#index = 521
#cv2.imshow('image1',img[index])
#print(names[index])
#cv2.waitKey(0)
