import os

PostAddressEnvKey = "POST_ADDRESS"
SerialPortNameEnvKey = "SERIAL_PORT_NAME"

DefaultPostAddress = "http://target.zapto.org/hit-miss-target-service"
DefaultSerialPortName = "/dev/ttyACM0"

def get_post_address():
    return os.getenv(PostAddressEnvKey, DefaultPostAddress)

def get_serial_port_name():
    return os.getenv(SerialPortNameEnvKey, DefaultSerialPortName)
