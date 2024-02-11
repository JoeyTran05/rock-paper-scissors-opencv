import cv2 as cv
import mediapipe as mp
import time
import math


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, frame, draw=True):
        """
        Detects hands in frame
        :param frame: camera frame per second
        :param draw: highlight hands
        :return: frame with highlighted hands
        """
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, hand_lms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def find_position(self, frame, handNo=0, draw=True):
        """
        Find the XYZ coordinates of the hand
        :param frame: camera frame per second
        :param handNo: index of hands
        :param draw: highlight the tip of fingers
        :return: XYZ coordinates of tip of fingers
        """
        self.lm_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(my_hand.landmark):
                # print(id, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)
        return self.lm_list

    def fingers_up(self):
        """
        Detects which finger is up
        :return: List of fingers up
        """
        fingers = []
        # Thumb
        if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
        # totalFingers = fingers.count(1)

    def find_distance(self, p1, p2, frame, draw=True, r=15, t=3):
        """
        Calculates distance between fingers
        :param p1: finger one
        :param p2: finger two
        :param frame: camera frame per second
        :param draw: highlight tip of fingers
        :param r:
        :param t:
        :return:
        """
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv.circle(frame, (x1, y1), 15, (255, 0, 255), cv.FILLED)
            cv.circle(frame, (x2, y2), 15, (255, 0, 255), cv.FILLED)
            cv.circle(frame, (cx, cy), 15, (255, 0, 255), cv.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            return length, frame, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = HandDetector()
    while True:
        success, frame = cap.read()
        frame = detector.find_hands(frame)
        lmList = detector.find_position(frame)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv.imshow('cap', frame)
        cv.waitKey(1)


if __name__ == "__main__":
    main()
