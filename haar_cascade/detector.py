from cascade import getNode
from imageMaking import creatingIntegForm
from readyFeatureNode import readyFeatureNode
from featureNode import *
import cv2 as cv
from numpy import append


percentsOfMistakesForClassifiers: list[float] = [0.5, 0.5, 0.5, 0.5, 0.5]

maxSizeW = 0
maxSizeH = 0

startSizeW = 200
startSizeH = 200
coef = 1.0
step = 20


def readInfo(filename):
     size: int
     infoArray: list[list[readyFeatureNode]] = []
     infoArray.append([])
     infoArray.append([])
     infoArray.append([])
     infoArray.append([])
     infoArray.append([])
     infoArray.append([])
     file = open(filename, mode="r")
     lines = file.readlines()
     size = len(lines) // 5
     for i in range(size):

         st = lines[i*5].split(" ")
         x = float(st[0])

         st = lines[i * 5 + 1].split(" ")
         y = float(st[0])

         st = lines[i * 5 + 2].split(" ")
         typeInt = int(st[0])
         type = FeatureType(int(st[0]))

         st = lines[i * 5 + 3].split(" ")
         intency = int(st[0])

         infoArray[int((typeInt)/2)].append(readyFeatureNode(type, x, y, intency))

     return infoArray

def checkWindow(matr, x1, y1, x2, y2,  info: list[list[readyFeatureNode]], listNum):
    if (listNum > 4):
        return True

    global coef
    cntMistakes: int = 0

    for node in info[listNum]:
        y = y1 + int(node.y * (y2-y1))
        x = x1 + int(node.x * (x2-x1))
        if (y <= maxSizeH
            and x <= maxSizeW):
            curFeat = getNode(node.type.value, matr, x, y, node.x, node.y)
            if (curFeat.intensity > node.average * 1.4
                or curFeat.intensity < node.average * 0.6):
                cntMistakes+= 1

    if int(len(info[listNum]) * percentsOfMistakesForClassifiers[listNum]) < cntMistakes:
        return False

    return True

def moving(info, matr):
    global coef
    coef = 1
    global startSizeH
    global startSizeW
    global step
    global maxSizeW
    global maxSizeH
    rectList: list[(int, int, int, int)] = []
    x: int = 0
    y: int = 0

    while (startSizeW * coef  <= maxSizeW
          and startSizeH * coef <= maxSizeH):
        x = 0
        y = 0

        while (x + startSizeW * coef <= maxSizeW):
            while(y + startSizeH * coef <= maxSizeH):
                if checkWindow(matr, x, y, x + startSizeW * coef, y + startSizeH * coef,  info, 0):
                    rectList.append((x, y, x + int(startSizeW * coef), y + int(startSizeW * coef)))
                y += startSizeH * coef

            x+=startSizeW * coef

        coef += 0.1

    return rectList

def makeRects(image, rectList: list[(int, int, int, int)]):
    for i in rectList:
        image = cv.rectangle(image, (i[0], i[1]), (i[2], i[3]), thickness=2, color=(0, 255, 0))

    return image

def detect(imageName):
    global startSizeW
    global startSizeH
    global maxSizeH
    global maxSizeW
    recList = []
    img = cv.imread(imageName)

    maxSizeH = img.shape[0]
    maxSizeW = img.shape[1]

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    maxSizeH = img.shape[0]
    maxSizeW = img.shape[1]

    matr = creatingIntegForm(img, maxSizeH, maxSizeW)

    infoModel = readInfo("model")
    info = moving(infoModel, matr)

    image = makeRects(img, info)
    cv.imshow("windowName", image)
    cv.waitKey()

