from mqtt_wrapper import MQTTWrapper
import emotions
import json
import sys

def loadUserConfig():
    with open(sys.path[0] + "/userConfig.json") as json_file:
        return json.load(json_file)

client = MQTTWrapper.fromJsonConfig(sys.path[0] + "/mqttConfig.json")
user = loadUserConfig()
emotions.setup()

while True:
    try:
        emotionsMap = emotions.getEmotions()
        dataToTransmit = { user["user"]: emotionsMap }
        client.publish(json.dumps(dataToTransmit))
        print(dataToTransmit)
    except emotions.NoFaceDetectedException:
        print("No face found!")
