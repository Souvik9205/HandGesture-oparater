import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self,mode=False, maxHands=2):
        self.mode = mode
        self.maxHands = maxHands

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

                # for id, lm in enumerate(handLms.landmark):
                #     h, w, c = img.shape
                #     cx, cy = int(lm.x * w), int(lm.y * h)
                #     cv2.circle(img, (cx, cy), 8, (77, 77, 255), cv2.FILLED )
def main():
    pTime = 0
    cap = cv2.VideoCapture(0)

    detector = handDetector()

    while True:
        success, img = cap.read()
        # Flip image horizontally to invert X-axis
        img = cv2.flip(img, 1)

        # Resize image to custom height and width
        img = cv2.resize(img, (640, 480))
        img = detector.findHands(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 87, 51), 2)
        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()