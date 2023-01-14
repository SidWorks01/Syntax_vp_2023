import cv2
import mediapipe as mp
from gen import Generator
import time
import numpy as np
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

_, frm = cap.read()
height = frm.shape[0]
width = frm.shape[1]
side = np.random.randint(30, 60)
gen = Generator(side,height, width)
s_init = False
s_time = time.time()
is_game_over = False

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

    cv2.putText(frm, "score: "+str(gen.score), (width - 250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0,0), 3)
    if not (s_init):
        s_init = True
        s_time = time.time()
    elif (time.time() - s_time) >= gen.genTime:
        s_init = False
        gen.create()

    frm.flags.writeable = False
    results = handModel.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    frm.flags.writeable = True

    gen.draw_Obs(frm)
    gen.update()

    if results.multi_hand_landmarks:
        pts = results.multi_hand_landmarks[0].landmark
        indexPoint = (int(pts[8].x * width), int(pts[8].y * height))
        gen.points(frm, indexPoint)
        if gen.check(indexPoint):
            is_game_over = True

            frm = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
            frm = cv2.blur(frm, (10, 10))
            cv2.putText(frm, "GAME_OVER!\nPress r to replay", (100, 100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            cv2.putText(frm, "Score : " + str(gen.score), (100, 180), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 0), 3)
            gen.score = 0

        cv2.circle(frm, indexPoint, 20, (0, 0, 255), -1)

    frm[0:125, 0:1280] = overLayList[0]
    frm[545:720, 0:1280]=overLayList[1]
    cv2.imshow("window", frm)

    if is_game_over:
        key_inp = cv2.waitKey(0)
        if (key_inp == ord('r')):
            is_game_over = False
            gen.obs = []
            gen.speed = 16
            gen.genTime = 1.2
        else:
            cv2.destroyAllWindows()
            cap.release()
            break

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break