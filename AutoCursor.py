import cv2
import numpy as np
import HandtrackingModule as htm
import pyautogui

wCam, hCam = 640, 480,
frameR = 100
smoothening = 1.5
pinch_threshold = 20

pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0
scrollcLocY, scrollpLocY = 0, 0
cLength01, pLength01 = 0, 0
isHolding = False

cap = cv2.VideoCapture(0)
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Video", wCam, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
cv2.moveWindow("Video", wScr-wCam, 0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        length12, img, lineInfo = detector.findDistance(8, 12, img)
        length01, img, lineInfo1 = detector.findDistance(4, 8, img)
        length02, img, lineInfo2 = detector.findDistance(4, 12, img)
        length03, img, lineInfo3 = detector.findDistance(4, 16, img)
        length04, img, lineInfo4 = detector.findDistance(4, 20, img)

        # print(length01, length02, length03, length04)

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR),
                      (wCam - frameR, hCam - frameR), (0, 0, 255), 2)

    # GESTURES LISTS ARE HERE -------------------------------------

        # [CURSOR MODE]
        if fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            pyautogui.moveTo(cLocX, cLocY)
            cv2.circle(img, (x1, y1), 12, (255, 255, 51), 3, 8, 0)
            pLocX, pLocY = cLocX, cLocY

        # [CLICK MODES]
        # LEFT CLICK MODE HERE ---------------
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[3] == 0 and fingers[4] == 0:
            if length12 < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           6, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='left')

        # RIGHT CLICK MODE HERE ---------------
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 and fingers[3] == 0 and fingers[4] == 0:
            if length12 < 25:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           6, (0, 255, 0), cv2.FILLED)
                pyautogui.click(button='right')

        # [SCROLL MODE]
        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
            maxScroll = 201
            minScroll = 26
            scrollcLocY = y1
            minMovement = 2
            # SCROLL DOWN

            if scrollcLocY > scrollpLocY and (scrollcLocY-scrollpLocY) > minMovement:
                scrollAmount = -(abs(-5*smoothening*(scrollcLocY-scrollpLocY)))
                if scrollAmount != 0 and not scrollAmount > -minScroll:
                    if scrollAmount < -maxScroll:
                        scrollAmount = -maxScroll
                    pyautogui.scroll(int(scrollAmount))
                    # print(scrollAmount)

            # SCROLL UP
            elif scrollcLocY < scrollpLocY and (scrollpLocY-scrollcLocY) > minMovement:
                scrollAmount = abs(5*smoothening*(scrollpLocY-scrollcLocY))
                if scrollAmount != 0 and not scrollAmount < minScroll:
                    if scrollAmount > maxScroll:
                        scrollAmount = maxScroll
                    pyautogui.scroll(int(scrollAmount))
                    # print(scrollAmount)

            scrollpLocY = scrollcLocY

        # [VOLUME CONTROL MODE]
        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 1:
            cLength01 = length01
            maxLength01 = 210
            minLength01 = 50

            if length01 > minLength01 and length01 < maxLength01:
                # VOLUME UP
                if cLength01 < pLength01:
                    # pyautogui.hotkey('volumeup')
                    pyautogui.hotkey('volumeup')
                # VOLUME DOWN
                elif cLength01 > pLength01:
                    pyautogui.hotkey('volumedown')
                    # pyautogui.hotkey('volumedown')
            cv2.circle(img, (lineInfo1[4], lineInfo1[5]),
                       6, (0, 255, 0), cv2.FILLED)
            pLength01 = cLength01

        # [DRAG AND DROP MODE]
        if (
            length01 < pinch_threshold and
            length02 < pinch_threshold and
            length03 < pinch_threshold and
            length04 < pinch_threshold
        ):
            if (isHolding == False):
                pyautogui.mouseDown(button='left')
                isHolding = True
        else:
            if (isHolding == True):
                pyautogui.mouseUp(button='left')
                isHolding = False

    cv2.imshow("Video", img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
