import cv2
import numpy as np

class Generator:
    def __init__(self, side, height, width):
        self.obs = []
        self.side = side
        self.width = width
        self.height = height
        self.speed = 16
        self.genTime = 1.2
        self.genTimeScore=2000
        self.score =0
        self.circleDim=[]
        # imageP1 = cv2.imread("Header2\ScoinBox.png")

    def create(self):
        rand_pty = np.random.randint(85, 635)
        rand_y = np.random.randint(85,635)
        self.obs.append(
            [self.width, self.side, rand_y, rand_y+self.side,False]
        )
        self.circleDim.append(
            [self.width,rand_pty,False]
        )

    def drawObs(self, frm):
        for i in self.obs:
            if (i[0] <= 0):
                continue

    def drawCircles(self,frm):
        for i in self.circleDim:
            if (i[0] <= 0):
                continue
            cv2.circle(frm, (i[0], i[1]), 20, (255, 0, 0), cv2.FILLED)
    def update(self):
        for i in self.obs:
            i[0] -= self.speed
            if (i[0] <= 0):
                self.obs.remove(i)
    def updateCircle(self):
        for i in self.circleDim:
            i[0] -= self.speed
            if (i[0] <= 0)or(i[2]==True):
                self.circleDim.remove(i)

    def check(self,indexPoint):
        for i in self.obs:
            if (indexPoint[0] >= i[0] and indexPoint[0] <= i[0] + self.side):
                if ((indexPoint[1] >= i[2]) and (indexPoint[1] <= i[3])):
                    return True
                else:
                    return False
        if ((indexPoint[1] <= 80) or (indexPoint[1] >= 635)):
            return True
        else:
            return False

    def points(self, img, indexPoint):
        for i in self.circleDim:
            if (((indexPoint[0] >= i[0] - 20 ) and (indexPoint[0] <= i[0] + 20)) and ((indexPoint[1] >= i[1] - 20 ) and (indexPoint[1] <= i[1] + 20))):
                self.score += 1
                i[2]=True
                if (self.score % 2 == 0):
                    self.speed += 4
                    self.genTimeScore -=0.08
                    self.genTime-=0.08
            return self.score


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