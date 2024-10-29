import RPi.GPIO as GPIO
from time import sleep

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


while(True):
    user_input = input()
    
    if user_input == 'w':
        print("going forward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    
    elif user_input == 's':
        print("going backward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
    
    elif user_input == 'r':
        print("now spinning right")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
        
    elif user_input == 'l':
        print("now spinning left")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)
    
    elif user_input == 'b':
        print("now stopped")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)
    
    elif user_input == 'e':
        print("GPIO Cleanup")
        GPIO.cleanup()
        break
