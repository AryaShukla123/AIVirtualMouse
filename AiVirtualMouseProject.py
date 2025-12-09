import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

wCam, hCam = 640, 480
frameR = 100
smoothening = 5

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
#print(wScr, hScr)


while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPositions(img)

    # 2. Get the tip of the index and middle finger
    if len(lmList)!=0:
        x1, y1 = lmList[8][3], lmList[8][4]

        x2, y2 = lmList[12][3], lmList[12][4]

        #print(x1,y1,x2,y2)

    # 3. Check which finger are up

        fingers = detector.fingersUp()
        #print(fingers)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Only Index Finger : Moving Mode

        if fingers[1]== 1 and fingers[2]==0:
            # 5. Convert Coordinates
            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)
            nx = lmList[8][1]  # normalized X
            ny = lmList[8][2]  # normalized Y

            x3 = np.interp(x1, (frameR, wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))

            # 6. Smoothen Values
            clocX = plocX +(x3 -plocX) /smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            x3 = max(0, min(wScr, x3))
            y3 = max(0, min(hScr, y3))

            autopy.mouse.move(wScr-clocX, clocY)
            h, w, c = img.shape
            cx, cy = int(x1 * w), int(y1 * h)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

    # 8. Both Index and Middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:

            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8,12,img)
            print(length)
            # 10. Click Mouse if distance is short
            if length < 30:
                cv2.circle(img, (x2, y2), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate

    cTime = time.time()
    fps = 1 / ( cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), org=(20,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(0,0,255), thickness=3 )

    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)