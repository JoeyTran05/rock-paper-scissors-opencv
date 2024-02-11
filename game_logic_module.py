import cv2 as cv
import hand_tracking_module as htm


class GameLogic:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.detector = htm.HandDetector()
        self.lmList = []
        self.fingersUp = False

    def choice_detector(self):
        """
        Detects which game hand is the user showing
        :return: the game hand of the player
        """
        if len(self.lmList) != 0:
            fingers = self.detector.fingers_up()

            if fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                return 'rock'
            elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                return 'scissors'
            elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                return 'paper'
            else:
                return 'none'
        return 'none'

    def main(self):
        success, frame = self.cap.read()
        frame = self.detector.find_hands(frame, draw=False)
        self.lmList = self.detector.find_position(frame, draw=False)

        # cv.imshow('cap', frame)
        # cv.waitKey(1)
