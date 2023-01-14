import cv2
import numpy as np
import HandTrackingModule as htm

class Generator:
    def __init__(self, side, height, width):
        self.obs = []
        self.side = side
        self.width = width
        self.height = height
        self.speed = 16
        hd = htm.handDetector()
        self.idx = hd.topidx
        self.landmarks = hd.findPosition
        self.genTime = 1.2
        self.score =0
    def create(self):
        rand_y = np.random.randint(125,485)
        self.obs.append(
            [self.width, self.side, rand_y, rand_y+self.side,False]
        )

    def draw_Obs(self, frm):
        for i in self.obs:
            if (i[0] <= 0):
                continue
            cv2.rectangle(frm, (i[0], i[2]), (i[0] + i[1], i[3]), (0, 255, 0), -1)

    def update(self):
        for i in self.obs:
            i[0] -= self.speed
            if (i[0] <= 0):
                self.obs.remove(i)
    def check(self,indexPoint):
        for i in self.obs:
            if (indexPoint[0] >= i[0] and indexPoint[0]<= i[0] + self.side):
                if ((indexPoint[1] <= i[2]) or (indexPoint[1] >= i[3])):
                    return True #true if hits
                else:
                    if not (i[4]):
                        i[4] = True

                    return False
        return False

    def points(self, img, indexPoint):
        rand_pty = np.random.randint(125, 545)
        rand_ptx = np.random.randint(0, self.width)

        cv2.circle(img, (rand_ptx, rand_pty), 10, (255, 0, 0), cv2.FILLED)
        if (((indexPoint[0] >= rand_ptx - 10 ) and (indexPoint[0] <= rand_ptx + 10))
                and ((indexPoint[1] >= rand_pty - 10 ) and (indexPoint[1] <= rand_pty + 10))):
            self.score += 1
            if (self.score % 10 == 0):
                self.speed += 4
                self.genTime -= 0.2
        return False

def main():
    pass
    # cap=cv2.VideoCapture(0)
    #
    # while cap.isOpened():
    #     success , img = cap.read()
    #     img=cv2.flip(img,1)
    #
    #     side = np.random.randint(30, 60)
    #     height = img.shape[0]
    #     width = img.shape[1]
    #
    #     gen=Generator(side,width,height)
    #     obs1=gen.create()
    #     for i in obs1:
    #         print (i)
    #     cv2.imshow("Image", img)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
if __name__=="__main__":
    main()