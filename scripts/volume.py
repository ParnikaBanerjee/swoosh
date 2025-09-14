import cv2
import numpy as np
import time
import handtracking as htm
import math

wcam,hcam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wcam) #propid 3 is width
cap.set(4,hcam) #propid 4 is width

detector=htm.handDetector(mindetconfidence=0.7)

while True:
    success,img=cap.read()#VideoCapture to start capturing video
    img=detector.findHands(img)
    landmarklist=detector.findPosition(img,draw=False)

    if len(landmarklist)!=0:
        #print(landmarklist[4],landmarklist[8])

        x1,y1=landmarklist[4][1],landmarklist[4][2]#thumb's x,y coordinates
        x2,y2=landmarklist[8][1],landmarklist[8][2]#index finger's x,y coordinates
        cx,cy=(x1+x2)//2,(y1+y2)//2 #center of the two circles

        cv2.circle(img,(x1,y1),10,(100,0,100),cv2.FILLED)#draw circle at thumb tip
        cv2.circle(img,(x2,y2),10,(100,0,100),cv2.FILLED)#draw circle at index tip
        cv2.circle(img,(cx,cy),10,(100,0,100),cv2.FILLED)#draw circle at index tip

        cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)#draw line between the two points

        length=math.hypot(x2-x1,y2-y1)#the hypotenuse of the two points to have a relation with the distance and using it to make it relatable to the volume  
        print(length)

        if length<50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        elif length>200:
            cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

    cv2.imshow("Image",img) #show the image on screen
    if cv2.waitKey(1) & 0xFF==ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break #wait for 1 millisecond before showing the next image