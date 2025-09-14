import cv2
import numpy as np
import time
import handtracking as htm
import math

#pycaw for volume control
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
'''print(f"Audio output: {device.FriendlyName}")
print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
volume.SetMasterVolumeLevel(-20.0, None)'''


volRange=volume.GetVolumeRange()
volume.GetMasterVolumeLevel()
minVol=volRange[0]
maxVol=volRange[1]

wcam,hcam=640,480

cap=cv2.VideoCapture(0)
cap.set(3,wcam) #propid 3 is width
cap.set(4,hcam) #propid 4 is width

detector=htm.handDetector(mindetconfidence=0.7)
converted_vol=0
volbar=400
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
        #print(length)

        #hand range: 20 to 300
        #volume range: -65 to 0
        converted_vol=np.interp(length,[20,300],[minVol,maxVol])
        volbar=np.interp(length,[20,300],[400,150])
        volperc=np.interp(length,[20,300],[0,100])
        #print(converted_vol)
        volume.SetMasterVolumeLevel(converted_vol,None)
        converted_vol=0

        if length<50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        elif length>200:
            cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)

        cv2.rectangle(img,(50,150),(85,400),(0,255,0),2)#volume bar
        cv2.rectangle(img,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)#volume bar
        cv2.putText(img, f'{int(volperc)} %', (40, 430), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Image",img) #show the image on screen
    if cv2.waitKey(1) & 0xFF==ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break #wait for 1 millisecond before showing the next image