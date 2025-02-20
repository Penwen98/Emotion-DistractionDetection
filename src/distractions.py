import numpy as np
import os
import cv2
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
import emotions
import datetime


model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(128,54,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))

model.load_weights(sys.path[0] + '/distraction-weights3.h5')


def setup():
    global distr_dict

    # dictionary which assigns each label a state
    distr_dict = {0: "Drinking", 1: "Brushing hair", 2: "Safe driving", 3: "Talking phone", 4: "Texting phone"}
    #distr_dict = {0: "Drinking", 1: "Safe driving", 2: "Talking phone", 3: "Texting phone"}

def predictionSetup(image):
    global end_time, saved_prediction
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=2)
    saved_prediction = model.predict(image)
    
class NoDriverDetectedException(Exception):
    def msg():
        return "No driver detected on the screen"

def getDistraction():
    # Find haar cascade to draw bounding box around person (upper body)
    ret = emotions.ret
    frame = emotions.frame
    if not ret:
        return 0
    
    #facecasc = cv2.CascadeClassifier(sys.path[0] + '/haarcascade_upperbody.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = facecasc.detectMultiScale(gray,scaleFactor=1.05, minNeighbors=5)
    resizedImg = np.expand_dims(np.expand_dims(cv2.resize(gray, (54, 128)), -1), 0)
    
    prediction = 0
    predictionSetup(resizedImg)
    while datetime.datetime.now() < end_time:
        if model.predict(resizedImg).all != saved_prediction.all:
            predictionSetup(resizedImg)
            break
        else:
            frame = emotions.frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resizedImg = np.expand_dims(np.expand_dims(cv2.resize(gray, (54, 128)), -1), 0)

    prediction = model.predict(resizedImg)
    
    data = {}
    if type(prediction) is np.ndarray:
        for distraction in distr_dict:
            data[distr_dict[distraction]] = round(prediction[0][distraction].item(), 8)
    else:
        raise NoDriverDetectedException
    
    return data