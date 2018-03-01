import pytest
import asyncio
import time
import serial
from boom.app import App

async def run_app():
    print("start of run_app")
    await asyncio.sleep(0.2)
    print("end of run_app")

async def main():
    print("start of main")
    task = asyncio.ensure_future(run_app())
    await asyncio.sleep(0.1)
    print("after task creation")
    await task
    print("end of main")

def test_app():
    #app = App("loop://", 0xF, 0xA, "http://localhost:11337", "1337")
    #app.run()
   behöver skicka in en skapad serial port i app så att jag kan trycka på dada
   wrappa i SampleReader eller nått sånt (SerialPortSampleReader)
   
    port = serial.serial_for_url("loop://", timeout=0)
    port.write(b'1234')
    result = port.read(4)
    print("result: {}".format(str(result)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


    assert False
