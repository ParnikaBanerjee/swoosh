import mediapipe as mp
import cv2
import time


class handDetector():
    def __init__(self,mode=False,maxhands=2,mindetconfidence=0.5,mintrackconfidence=0.5): #contructor for turning this program into a proper module 
        self.mode=mode
        self.maxhands=maxhands
        self.mindetconfidence=mindetconfidence
        self.mintrackconfidence=mintrackconfidence
        self.mphands=mp.solutions.hands
        self.hands = self.mphands.Hands(
                        static_image_mode=self.mode,
                        max_num_hands=self.maxhands,
                        min_detection_confidence=self.mindetconfidence,
                        min_tracking_confidence=self.mintrackconfidence
)
        self.skeletondraw=mp.solutions.drawing_utils
    
    def findHands(self,img,draw=True):
        imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgrgb)
        #print(self.results.multi_hand_landmarks)


        if self.results.multi_hand_landmarks:
            for handMLM in self.results.multi_hand_landmarks:
                if draw:
                    self.skeletondraw.draw_landmarks(img, handMLM, self.mphands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img, handNumber=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNumber]
            for id,lm in enumerate(myhand.landmark):#id is the location of hand points from hand map.png, lm is the x,y position of that id(handpoint) on the img window
                        #print(id,lm)
                        h,w,c=img.shape
                        centerx,centery=int(lm.x*w),int(lm.y*h)
                        #print(id, centerx,centery)
                        lmList.append([id,centerx,centery])
                        if draw:
                            #if id==0: #to map points from hand map.png, like 0 is the start of the palm and so on
                            cv2.circle(img,(centerx,centery),15,(255,0,0),cv2.FILLED)

        return lmList

def main():
    cam=cv2.VideoCapture(0)

    detector=handDetector()
    while True:
        success,img=cam.read()
        img=detector.findHands(img)
        lmList=detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[0])#helps find landmarks of a specific handpoint id
        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF==ord('q') or cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:
            break

if __name__=='__main__':
    main()