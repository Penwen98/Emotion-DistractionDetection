from mqtt_wrapper import MQTTWrapper
import emotions
import json
import sys
import time

def loadUserConfig():
    with open(sys.path[0] + "/userConfig.json") as json_file:
        return json.load(json_file)

client = MQTTWrapper.fromJsonConfig(sys.path[0] + "/mqttConfig.json")
user = loadUserConfig()
emotions.setup()

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
        client.publish(json.dumps(dataToTransmit))
        print(dataToTransmit)
        time.sleep(1)
    except emotions.NoFaceDetectedException:
        print("No face found!")
