import cv2
import numpy as np
import utilities
import WebcamModule

curveList = []
avgVal=10

def getLaneCurve(img):

    imgCopy = img.copy()
    imgResult = img.copy()


    # Turning our image into HSV image space with thresholding. Isolating our lane.
    imgThres = utilities.thresholding(img)


    
    # Warping our webcam feed to get a top down view granting us better histogram values.
    hT, wT, c = img.shape
    points = utilities.valTrackbars()
    imgWarp = utilities.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utilities.drawPoints(imgCopy, points)

    # Getting the values of the warped thresheld image and getting all the values of the histogram
    middlePoint,imgHist = utilities.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    curveAveragePoint,imgHist = utilities.getHistogram(imgWarp,display=True,minPer=0.9)
    curveRaw = curveAveragePoint - middlePoint
    curveList.append(curveRaw)
    if len(curveList)>avgVal:
        curveList.pop(0)

    # Getting sum of all of histogram subtracting both sides from each other.
    curve = int(sum(curveList)/len(curveList))

    # Displaying all our images
    imgInvWarp = utilities.warpImg(imgWarp, points, wT, hT,inv = True)
    imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
    imgInvWarp[0:hT//3,0:wT] = 0,0,0
    imgLaneColor = np.zeros_like(img)
    imgLaneColor[:] = 0, 255, 0
    imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
    imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
    midY = 450
    cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
    cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
    cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
    for x in range(-30, 30):
        w = wT // 20
        cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
        
    cv2.imshow('Result',imgResult)
    cv2.imshow('Thres', imgThres)
    cv2.imshow('Warp', imgWarp)
    cv2.imshow('Warp Points', imgWarpPoints)
    cv2.imshow('Histogram', imgHist)


    # NORMALIZATION getting our curve value
    curve = curve/100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve

if __name__ == '__main__':
    initialTrackbarVals = [102, 80, 30, 214]
    utilities.initializeTrackbars(initialTrackbarVals)
    while True:

        img = WebcamModule.getImg()
        curve = getLaneCurve(img,display=0)
        print(curve)

        cv2.waitKey(1) 
