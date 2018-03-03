import pytest
import asyncio
import time
import serial
from boom.app import App
from boom.serial_port import SerialPort
from http.server import HTTPServer, BaseHTTPRequestHandler

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("POST!!")

async def run_http_server(server):
    print("serve_forever")
    server.serve_forever()
    print("efter serve_forever")

async def run_app(app):
    app.run()

async def run_test():
    serialPort = SerialPort("loop://")
    app = App(serialPort, 0xFFFF, 0xA, "http://localhost:11337", "1337")
    
    server = HTTPServer(("localhost", 11337), PostHandler)
    server.allow_reuse_address = True
    
    app_task = asyncio.ensure_future(run_app(app))
    #http_task = ayncio.ensure_future(run_http_server(server))

    serialPort.write(b',1234')
    
    server.shutdown()
    serialPort.serialPort.close()
    app.stop()
    #await http_task
    #await app_task

def test_app():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_test())

    assert False
