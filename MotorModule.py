import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, en_A, in1, in2, en_B, in3, in4):
        self.en_A = en_A
        self.in1 = in1
        self.in2 = in2
        self.en_B = en_B
        self.in3 = in3
        self.in4 = in4
        GPIO.setup(self.en_A, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.en_B, GPIO.OUT)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        self.power_a = GPIO.PWM(self.en_A,100)
        self.power_a.start(0)
        self.power_b = GPIO.PWM(self.en_B,100)
        self.power_b.start(0)

    def move(self, speed=0.5, turn=0, t=0):
        speed  *= 100
        turn *= 100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed>100: leftSpeed = 100
        elif leftSpeed<-100: leftSpeed = -100
        if rightSpeed>100: rightSpeed = 100
        elif rightSpeed<-100: rightSpeed = -100

        self.power_a.ChangeDutyCycle(abs(leftSpeed))
        self.power_b.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed > 0:
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)
        else:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)

        if rightSpeed > 0:
            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        
        else:
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
        sleep(t)
    
    def stop(self,t=0):
        self.power_a.ChangeDutyCycle(0)
        self.power_b.ChangeDutyCycle(0)
        sleep(t)


in1 = 17
in2 = 27
in3 = 23
in4 = 24
en_A = 4
en_B = 25
temp1 = 1


def main():
    motor.move(0.5,0,2)
    motor.stop(2)
    motor.move(-0.5,0,2)
    motor.stop(2)
    motor.move(0,0.5,2)
    motor.move(2)
    motor.move(0,-0.5,2)
    motor.move(2)

if __name__ == '__main__':
    motor = Motor(4,17,27,25,23,24)
    main()