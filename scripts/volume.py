import cv2
import numpy as np
import time
import handtracking as htm

wcam,hcam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wcam) #propid 3 is width
cap.set(4,hcam) #propid 4 is width

detector=htm.handDetector(mindetconfidence=0.7)

while True:
    success,img=cap.read()#VideoCapture to start capturing video
    img=detector.findHands(img)
    landmarklist=detector.findPosition(img,draw=False)
    print(landmarklist)
    cv2.imshow("Image",img) #show the image on screen
    if cv2.waitKey(1) & 0xFF==ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break #wait for 1 millisecond before showing the next image