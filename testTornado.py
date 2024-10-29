#! /usr/bin/python
import tornado.ioloop
import tornado.web
import tornado.websocket
import RPi.GPIO as GPIO
from time import sleep
import os

GPIO.setwarnings(False)

in1 = 17
in2 = 27
in3 = 23
in4 = 24
en_A = 4
en_B = 25
temp1 = 1


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)


GPIO.setup(en_A,GPIO.OUT)
GPIO.setup(en_B,GPIO.OUT)


GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


power_a = GPIO.PWM(en_A,GPIO.HIGH)
power_a.start(100)
power_b = GPIO.PWM(en_B,GPIO.HIGH)
power_b.start(100)


class PiCarHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket Opened")
    
    def on_message(self, message):
        print("Received message:", message)
        
        if message == "w":
            print("Now going forward")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            
        elif message == "s":
            print("Now going backward")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            
        elif message == "r":
            print("Now spining to the right")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            
        elif message == "l":
            print("Now spinning to the left")
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            
        elif message == "b":
            print("Now stopped")
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            
        elif message == "e":
            GPIO.cleanup()

    def on_close(self):
        print("WebSocket closed")
        GPIO.cleanup()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("testServer.html")
    
app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/ws", PiCarHandler),  # WebSocket endpoint
], template_path=os.path.dirname(__file__))

if __name__ == "__main__":
    app.listen(8080)
    print("Server started on http://localhost:8080")
    tornado.ioloop.IOLoop.instance().start()
