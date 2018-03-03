from boom.serial_port import SerialPort
from boom.message_parser import MessageParser
from boom.simple_hit_detector import SimpleHitDetector
from boom.poster import Poster

class App:
    def __init__(self, serialPort, maxValue, hitValue, postAddress, targetId):
        self.runApp = True
        self.serialPort = serialPort
        self.messageParser = MessageParser()
        self.hitDetector = SimpleHitDetector(maxValue, hitValue)
        self.poster = Poster(postAddress, targetId)
        
    def run(self):
        while self.runApp:
            readBytes = self.serialPort.read(5000)
            messages = self.messageParser.parse(readBytes)
            if self.hitDetector.detect_hit(messages):
                self.poster.post_hit(self.hitDetector.get_last_hit_fraction())

    def stop(self):
        self.runApp = False