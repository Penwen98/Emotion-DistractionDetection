from mqtt_wrapper import MQTTWrapper
import emotions
import distractions
import json
import sys
import time

def loadUserConfig():
    with open(sys.path[0] + "/userConfig.json") as json_file:
        return json.load(json_file)

emotions_client = MQTTWrapper.fromJsonConfig(sys.path[0] + "/emotionsMqttConfig.json")
distractions_client = MQTTWrapper.fromJsonConfig(sys.path[0] + "/distractionsMqttConfig.json")
user = loadUserConfig()
emotions.setup()
distractions.setup()

while True:
    try:
        emotionsMap = emotions.getEmotions()
        dataToTransmit = { 
            user["user"]: {
                "neutral": emotionsMap["Neutral"],
                "happiness": emotionsMap["Happy"],
                "surprise": emotionsMap["Surprised"],
                "sadness": emotionsMap["Sad"],
                "anger": emotionsMap["Angry"],
                "disgust": emotionsMap["Disgusted"],
                "fear": emotionsMap["Fearful"]
            } 
        }
        emotions_client.publish(json.dumps(dataToTransmit))
        print(dataToTransmit)
        time.sleep(1)
    except emotions.NoFaceDetectedException:
        print("No face found!")

    try:
        distractionMap = distractions.getDistraction()
        dataToTransmit2 = { 
            user["user"]: {
                "drinking": distractionMap["Drinking"],
                "brushing_hair": distractionMap["Brushing hair"],
                "safe_driving": distractionMap["Safe driving"],
                "talking_phone": distractionMap["Talking phone"],
                "texting_phone": distractionMap["Texting phone"]
            } 
        }
        distractions_client.publish(json.dumps(dataToTransmit2))
        print(dataToTransmit2)
        time.sleep(1)
    except distractions.NoDriverDetectedException:
        print("No driver found!")
        
