import cv2
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(raw={"size":(1640,1232)},main={"format":'RGB888',"size":(640,480)}))
picam2.start()
time.sleep(2)


def getImg(display=False, size=[480, 240]):
    img = picam2.capture_array()
    img = cv2.resize(img, (size[0], size[1]))
    if display:
        cv2.imshow('IMG', img)
    return img

if __name__== '__main__':
  try:
    while True:
      img = getImg(True)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  finally:
        picam2.stop()
        picam2.close()
        cv2.destroyAllWindows()


