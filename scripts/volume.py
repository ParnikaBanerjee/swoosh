import cv2
import numpy as np
import time

cap=cv2.VideoCapture(0)

    success,img=cap.read()
    cv2.imshow("Img",img)
    cv2.waitKey(0)