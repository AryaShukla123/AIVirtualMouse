import cv2
import mediapipe as mp
import math


class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.lmList = []

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPositions(self, img, handNo=0, draw=True):
        self.lmList = []
        xList = []
        yList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            h, w, _ = img.shape

            for id, lm in enumerate(myHand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)  # pixel coords
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, lm.x, lm.y, cx, cy])


                if draw:
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = (xmin, ymin, xmax, ymax)

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

            return self.lmList, bbox

        return self.lmList, []

    def fingersUp(self):

        if not hasattr(self, 'lmList') or len(self.lmList) == 0:
            return []

        fingers = []


        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)


        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


    def findDistance(self, p1, p2, img, draw=True):
        x1, y1 = self.lmList[p1][3], self.lmList[p1][4]  # pixel coords
        x2, y2 = self.lmList[p2][3], self.lmList[p2][4]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, (x1, y1, x2, y2)

