import datetime
import requests

class Poster:
    def __init__(self, postAddress, targetId):
        self.postAddress = postAddress
        self.targetType = "hit_miss_target"
        self.targetId = targetId    

    def post_hit(self, vibrationFactor):
        requests.post(self.postAddress, json =
        {
            "target_type": self.targetType,
            "target_id": self.targetId,
            "event": "vibration_triggered",
            "vibration_factor": vibrationFactor,
            "timestamp": str(datetime.datetime.now())
        })
