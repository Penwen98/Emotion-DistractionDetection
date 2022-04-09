from mqtt_wrapper import MQTTWrapper
import emotions
import json
import sys
import time

client = MQTTWrapper.fromJsonConfig(sys.path[0] + "/mqttConfig.json")
emotions.setup()

while True:
    try:
       data = emotions.getEmotions()
       client.publish(json.dumps(data))
    except emotions.NoFaceDetectedException:
        print("No face found!")
    time.sleep(1)