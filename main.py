import cv2
from utils.HandDetector import HandDetector
import socket

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://172.16.0.145:4747/mjpegfeed')

W = 8 #Real size of red line in cm
f = 630 #Focal lenght (can be calculated)

# How to calculate focal lenght:
# d - distance in cm
# w - width in pixels
# W - real width in cm
# f = (d*w)/W


scrnwidth = 640
scrnheight = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, scrnwidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, scrnheight)

detector = HandDetector(maxHands=2, detectionCon=0.1)

#communication part
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketAdressPort = ('localhost', 6967)

def fdfc(f,W,p1,p2):
    """
        fdfc - find distance from camera
        
        f - focal lenght
        W - real length in cm
        w - width in pixels
        F - focal length

        p1 - point 1 (x,y)
        p2 - point 2 (x,y)

    """

    "detector finds distance between two points in pixels"
    w,_=detector.findDistance(p1,p2)

    d = W*f/w
    
    return d

while True:

    "Get image frame"
    success,img  =  cap.read()

    #img2 = img.copy()

    data=""

    "Find the hand and its landmarks"
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            "Wrist position"
            lx, ly = hand["lmList"][0][0], hand["lmList"][0][1]

            "17th point"
            rx, ry = hand["lmList"][17][0], hand["lmList"][17][1]
            d = fdfc(f,W,(lx,ly),(rx,ry))

            "Red line between wrist and 17th point"
            cv2.line(img, (lx, ly), (rx, ry), (0, 0, 255), 3)
            
            scrnCenter_x = scrnwidth/2
            scrnCenter_y = scrnheight/2

            "center point between wrist and 17th point"
            center_x = abs((rx+lx)/2)
            center_y = abs((ry+ly)/2)


            X_virtual = -(center_x-scrnCenter_x)
            Y_virtual = -(center_y-scrnCenter_y)

            X_real = X_virtual*(W/d)
            Y_real = Y_virtual*(W/d)

            Z_real = d

            "debug data"
            cv2.putText(img, f'X{round(X_real)}cm', (lx, ly - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            cv2.putText(img, f'Y{round(Y_real)}cm', (lx, ly - 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            cv2.putText(img, f'Z{round(Z_real)}cm', (lx, ly - 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

            lmArray=[]
            for lm in hand['lmList']:
                lmArray.extend([lm[0],scrnheight-lm[1],lm[2]])

            data+=f"{hand['type']}:{[X_real,Y_real,Z_real]};"
            #data+=f"{hand['type']}:{[X_real,Y_real,Z_real]}:{lmArray};"
            #data+=f"{hand['type']}:{[round(X_real),round(Y_real),round(Z_real)]};"

        print(data)

        socket.sendto(str.encode(data),socketAdressPort)

    cv2.imshow("img",img)
    #cv2.imshow("img2",img2)
    cv2.waitKey(1)