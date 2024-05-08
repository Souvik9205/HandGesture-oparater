# [DRAG AND DROP MODE]
        # if (
        #     length01 < pinch_threshold and
        #     length02 < pinch_threshold and
        #     length03 < pinch_threshold and
        #     length04 < pinch_threshold
        # ):
        #     cv2.putText(img, "DRAG & DROP MODE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 6)
        #     cv2.putText(img, "DRAG & DROP MODE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 3)
        #     if (isHolding == False):
        #         pyautogui.mouseDown(button='left')
        #         isHolding = True
        # else:
        #     if (isHolding == True):
        #         pyautogui.mouseUp(button='left')
        #         isHolding = False