import emotions
import json


emotions.setup()

data = {}
try:
    data = emotions.getEmotions()
except emotions.NoFaceDetectedException:
    print("No face found!")

print(json.dumps(data))
