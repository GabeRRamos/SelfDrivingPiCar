import cv2
import numpy as np


# Thresholding for HSV image space
def thresholding(img):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_Whites = np.array([85,0,0])
    upper_Whites = np.array([255,213,255])
    newImg = cv2.inRange(img_HSV, lower_Whites, upper_Whites)
    return newImg

# Warping the image to be top down
def warpImg(img, points, w, h, inv = False):
    points1 = np.float32(points)
    points2 = np.float32([[0,0], [w,0], [0,h], [w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(points2, points1)
    else:
        matrix = cv2.getPerspectiveTransform(points1, points2)
    warpedImg = cv2.warpPerspective(img, matrix, (w,h))
    return warpedImg

def nothing(a):
    pass


def initializeTrackbars(initialTrackbarVals, wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", initialTrackbarVals[0], wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", initialTrackbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", initialTrackbarVals[2], wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", initialTrackbarVals[3], hT, nothing)

def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop), (widthBottom, heightBottom), (wT-widthBottom, heightBottom)])
    return points

# Draw points for warping
def drawPoints(img, points):
    for x in range(4):
        cv2.circle(img,(int(points[x][0]), int(points[x][1])), 15, (0,0,255), cv2.FILLED)
    return img

# Function that allows to get values of the histogram
def getHistogram(img,minPer=0.1, display=False, region=1):
    if region == 1:
        histogram_Values = np.sum(img, axis=0)
    else:
        histogram_Values = np.sum(img[img.shape[0]//region:,:], axis=0)
    maxValue = np.max(histogram_Values)
    minValue = minPer*maxValue

    indexArray = np.where(histogram_Values>=minValue)
    basePoint = int(np.average(indexArray))

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1],3), np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape[0]),(x,int(img.shape[0]-intensity//255//region)),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return basePoint, imgHist
    return basePoint
    
# Function so that you can view all the images simultaneously next to each other.
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
