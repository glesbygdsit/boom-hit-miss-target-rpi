class SimpleHitDetector:
    def __init__(self, maxValue, hitValue):
        self.maxValue = maxValue
        self.hitValue = hitValue
        self.lastHitMaxValue = 0
    
    def detect_hit(self, values):
        hits = [x for x in values if x >= self.hitValue]
        if len(hits):
            self.lastHitMaxValue = max(hits)
            return True

        return False
    
    def get_last_hit_fraction(self):
        return self.lastHitMaxValue / self.maxValue

    def set_hit_value(self, hitValue):
        self.hitValue = hitValue
