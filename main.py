import cv2
import mediapipe as mp
from gen import Generator
import time
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

_, frm = cap.read()
height = frm.shape[0]
width = frm.shape[1]
side = 60
gen = Generator(side,height, width)
s_init = False
s_time = time.time()
isGameOver = False

hand = mp.solutions.hands
handModel = hand.Hands(max_num_hands=1)
drawing = mp.solutions.drawing_utils



folderPath = "Header2"
myList = os.listdir(folderPath)
overLayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)


while cap.isOpened():
    startS = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)
    imgBack = cv2.imread("Header2\LBack.png")
    addedImage = cv2.addWeighted(frm, 0.8, imgBack, 0.2, 0)
    cv2.putText(addedImage, "score: "+str(gen.score), (width - 250,150 ), 1, 1.5, (255, 0,0), 3)
    if not (s_init):
        s_init = True
        s_time = time.time()
    elif (time.time() - s_time) >= gen.genTime:
        s_init = False
        gen.create()
        # starting Overlay dynamic
        # rows, cols, channels = imageP1.shape
        # roi = addedImage[gen.circleDim[0]:rows, gen.circleDim[1]:cols]
        # img2gray = cv2.cvtColor(addedImage, cv2.COLOR_BGR2GRAY)
        # ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
        # mask_inv = cv2.bitwise_not(mask)
        # img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        # img2_fg = cv2.bitwise_and(addedImage, addedImage, mask=mask)
        # out_img = cv2.add(img1_bg, img2_fg)
        # addedImage = imageP1[0:rows, 0:cols]

    addedImage.flags.writeable = False
    results = handModel.process(cv2.cvtColor(addedImage, cv2.COLOR_BGR2RGB))
    addedImage.flags.writeable = True

    gen.drawObs(addedImage)
    gen.drawCircles(addedImage)
    gen.update()
    gen.updateCircle()


    if results.multi_hand_landmarks:
        pts = results.multi_hand_landmarks[0].landmark
        indexPoint = (int(pts[8].x * width), int(pts[8].y * height))
        score=gen.points(frm, indexPoint)
        if gen.check(indexPoint):
            isGameOver = True
            addedImage = cv2.cvtColor(addedImage, cv2.COLOR_BGR2HSV)
            addedImage = cv2.blur(addedImage, (10, 10))
            cv2.putText(addedImage, "GAMEOVER!!    Press r to replay", (20, 150), 1, 2, (255, 0, 0), 3)
            cv2.putText(addedImage, "Score : " + str(gen.score), (1100, 150), 1, 2, (255, 0, 0), 3)
            gen.score = 0
        cv2.circle(addedImage, indexPoint, 6, (0, 0, 255), -1)



    addedImage[0:85, 0:1280] = overLayList[2]
    addedImage[635:720, 0:1280]=overLayList[0]


    cv2.imshow("window", addedImage)

    if isGameOver:
        keyInp = cv2.waitKey(0)
        if (keyInp == ord('r')):
            isGameOver = False
            gen.obs = []
            gen.circleDim=[]
            gen.speed = 16
            gen.genTime = 1.2
            gen.genTimeScore=2000
        else:
            cv2.destroyAllWindows()
            cap.release()
            break

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break