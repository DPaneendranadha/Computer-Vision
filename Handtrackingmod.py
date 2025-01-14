import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self,mode=False, maxhands=2 , detectioncon =0.5 , trackcon =0.5):
        self.mode = mode
        self.max_num_hands = maxhands
        self.min_detection_con = detectioncon
        self.min_tracking_con = trackcon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode , self.max_num_hands ,self.min_detection_con,self.min_tracking_con)
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handlms.landmark):
                    # print(id ,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    print(id, cx, cy)
                    if id % 4 == 0:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 0))
                if draw :
                   self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img , handno = 0 , draw = True):
        lmlist =[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id , lm in enumerate(myhand.landmark):
                h, w , c = img.shape
                cx , cy = int(lm.x*h) ,int( lm.y*w)
                lmlist.append([id , cx, cy])
                if draw:
                    cv2.circle( img , (cx,cy), 15 , (255,0,255), cv2.FILLED)
        return lmlist


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findPosition(img)
        if len(lmlist) !=0:
            print(lmlist[4])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
      main()