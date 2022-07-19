# -*- coding: utf-8 -*-
"""mainTrain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LVvvzuGtKCt_pnDinHBz9pC6qzUmX4YZ
"""

# import modules 
import cv2
import os
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import normalize
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils.np_utils import to_categorical

# Initialising the directory
image_directory = '/content/Datasets/'
no_tumor = os.listdir(image_directory+'/no/')
yes_tumor = os.listdir(image_directory+'/yes/')
dataset=[]
label=[]
Input_size = 64

for i, image_name in enumerate(no_tumor):
  if(image_name.split('.')[1] == 'jpg'):
    images = cv2.imread(image_directory+'/no/'+image_name)
    images = Image.fromarray(images, mode='RGB')
    images = images.resize((Input_size,Input_size))
    dataset.append(np.array(images))
    label.append(0)

for i, image_name in enumerate(yes_tumor):
  if(image_name.split('.')[1] == 'jpg'):
    images = cv2.imread(image_directory+'/yes/'+image_name)
    images = Image.fromarray(images, mode='RGB')
    images = images.resize((Input_size,Input_size))
    dataset.append(np.array(images))
    label.append(1)

dataset = np.array(dataset)
label = np.array(label)

x_train, x_test, y_train, y_test = train_test_split(dataset, label, test_size=0.2, random_state=0)

x_train = normalize(x_train, axis=1)
x_teat = normalize(x_test, axis=1)

y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)

"""# ***Model Building***"""

model = Sequential()

# we are building 3 by 64 layer
#layer1
model.add(Conv2D(64, (5,5), input_shape=(Input_size, Input_size, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#layer2
model.add(Conv2D(64, (5,5), kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

#layer3
model.add(Conv2D(64, (5,5), kernel_initializer='he_uniform'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(2))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=16, verbose=1, epochs=20, validation_data=(x_test, y_test), shuffle=False)

loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
loss_v, accuracy_v = model.evaluate(x_test, y_test, verbose=1)
print("Validation: accuracy = %f  ;  loss_v = %f" % (accuracy_v*100, loss_v))
print("Test: accuracy = %f  ;  loss = %f" % (accuracy*100, loss))

model.save('BrainTumorModel.h5')