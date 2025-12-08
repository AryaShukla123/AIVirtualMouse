import cv2
import mediapipe as mp


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
        lmList = []
        xList = []
        yList = []
        bbox = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            h, w, c = img.shape

            for id, lm in enumerate(myHand.landmark):

                nx, ny = lm.x, lm.y
                xList.append(nx)
                yList.append(ny)
                lmList.append([id, nx, ny])

                if draw:

                    cx, cy = int(nx * w), int(ny * h)
                    cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                # Convert normalized to pixels
                xmin_pixel = int(xmin * w)
                ymin_pixel = int(ymin * h)
                xmax_pixel = int(xmax * w)
                ymax_pixel = int(ymax * h)

                cv2.rectangle(img, (xmin_pixel - 20, ymin_pixel - 20),
                              (xmax_pixel + 20, ymax_pixel + 20),
                              (0, 255, 0), 2)

        self.lmList = lmList

        return lmList, bbox



    def fingersUp(self):

        if not hasattr(self, 'lmList') or len(self.lmList) == 0:
            return []

        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
