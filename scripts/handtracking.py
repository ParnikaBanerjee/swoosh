import mediapipe as mp
import cv2
import time

cam=cv2.VideoCapture(0)

mphands=mp.solutions.hands
hands=mphands.Hands()
skeletondraw=mp.solutions.drawing_utils

while True:
    success,img=cam.read()

    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgrgb)
    print(results.multi_hand_landmarks)


    if results.multi_hand_landmarks:
        for handMLM in results.multi_hand_landmarks:
            for id,lm in enumerate(handMLM.landmark):
                print(id,lm)

            skeletondraw.draw_landmarks(img, handMLM, mphands.HAND_CONNECTIONS)



    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF==ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
        break