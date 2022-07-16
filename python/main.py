import cv2
from cvzone.HandTrackingModule import HandDetector
import json
import cvzone
import socket
cap = cv2.VideoCapture(0)

scrnwidth = 640
scrnheight = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, scrnwidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, scrnheight)

detector = HandDetector(maxHands=2, detectionCon=0.1)

#communication part
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketAdressPort = ('localhost', 6967)

def fdfc(f,W,p1,p2):
    "Distance from camera to object"
    "W is real length in cm"
    "F is focal length in pixels"
    w,_=detector.findDistance(p1,p2)
    return W*f/w

while True:
    success,img  =  cap.read()

    data=""

    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            lx, ly = hand["lmList"][0][0], hand["lmList"][0][1]
            rx, ry = hand["lmList"][17][0], hand["lmList"][17][1]
            d = fdfc(630,8,(lx,ly),(rx,ry))
            
            scrnCenter_x = scrnwidth/2
            scrnCenter_y = scrnheight/2

            center_x = abs((rx+lx)/2)
            center_y = abs((ry+ly)/2)

            X_virtual = -(center_x-scrnCenter_x)
            Y_virtual = -(center_y-scrnCenter_y)
            X_real = X_virtual*(8/d)
            Y_real = Y_virtual*(8/d)

            Z_real = d

            cv2.putText(img, f'X{round(X_real)}cm', (lx, ly - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            cv2.putText(img, f'Y{round(Y_real)}cm', (lx, ly - 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            cv2.putText(img, f'Z{round(Z_real)}cm', (lx, ly - 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

            lmArray=[]
            for lm in hand['lmList']:
                lmArray.extend([lm[0],scrnheight-lm[1],lm[2]])


            data+=f"{hand['type']}:{[X_real,Y_real,Z_real]}:{lmArray};"
        

        print(round(X_real),round(Y_real),round(Z_real))

        socket.sendto(str.encode(data),socketAdressPort)

    cv2.imshow("img",img)
    cv2.waitKey(1)