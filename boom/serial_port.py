import serial

class SerialPort:
    def __init__(self, port="/dev/ttyACM0", baudrate=115200, timeout=0):
        self.serialPort = serial.serial_for_url(
            port, baudrate=baudrate, timeout=timeout)

    def read(self, bytesToRead=1):
        return self.serialPort.read(bytesToRead)

    def write(self, data):
        return self.serialPort.write(data)