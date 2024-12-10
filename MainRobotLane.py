from MotorModule import Motor
from lanePicker import getLaneCurve
import WebcamModule
import cv2

# Sets up Motor class
# Sends signals out to corresponding GPIO pins
motor = Motor(4,17,27,25,23,24)


def main():

    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img)

    sen = 1.5
    maxVAL = 0.5
    if curveVal>maxVAL:
        curveVal = maxVAL
    if curveVal<-maxVAL:
        curveVal=-maxVAL
    
    if curveVal>0:
        sen = 1
        if curveVal <0.1: curveVal = 0
    else:
        if curveVal>-0.1: curveVal = 0

    
    motor.move(0.20,-curveVal*sen,0.05)
    cv2.waitKey(1)

if __name__ == '__main__':
    while True:
        main()
