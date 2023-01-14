import cv2
import numpy as np
import time
import os
import mediapipe as mp
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

brushThickness = 10
eraserThickness = 100
xp, yp = 0, 0
drawingColor = (0, 0, 0)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

detector = htm.handDetector(detectionCon=0.8)

folderPath = "Header"
myList = os.listdir(folderPath)
overLayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)
header = overLayList[8]

while cap.isOpened():
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x0, y0 = lmList[4][1:]
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
    #     print(lmlist)

        fingers = detector.fingercheck()
        # print(fingers)

        if fingers[1] and fingers[2]:
            xp,yp=0,0
            cv2.ellipse(img, (int(((x1+x2)/2)), (int(((y1+y2)/2)))), ((abs(int((x2-x1)/2))), abs(int((y2-y1)))),0,0,360, (255, 0 , 255), cv2.FILLED)
            if y1 < 125:
                if 128 < x1 < 256:
                    header = overLayList[0]
                    drawingColor = (0, 0, 255)
                elif 256 < x1 < 384:
                    header = overLayList[1]
                    drawingColor = (0,255,0)
                elif 384 < x1 < 512:
                    header = overLayList[2]
                    drawingColor = (255,255,0)
                elif 512 < x1 < 640:
                    header = overLayList[3]
                    drawingColor = (255,0,255)
                elif 640 < x1 < 768:
                    header = overLayList[4]
                    drawingColor = (255,0,0)
                elif 768 < x1 < 896:
                    header = overLayList[5]
                    drawingColor = (0,128,0)
                elif 896 < x1 < 1024:
                    header = overLayList[6]
                    drawingColor = (0,128,128)
                elif 1024 < x1 < 1152:
                    header = overLayList[7]
                    drawingColor = (255,0,0)
                elif 1152 < x1 < 1280:
                    header = overLayList[8]
                    drawingColor = (0,0,0)
            # print('Selection Mode')

        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            # print('Drawing mode')
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawingColor == (0, 0, 0):

                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawingColor, eraserThickness)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawingColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawingColor, brushThickness)
            xp, yp = x1, y1
        else:
            xp,yp=0,0
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:125, 0:1280] = header
    img = cv2.addWeighted(img, 0.8, imgCanvas,0.8 , 0)
    cv2.imshow("Test", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()





