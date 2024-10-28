from cascade import getNode
from imageMaking import creatingIntegForm
from readyFeatureNode import readyFeatureNode
from featureNode import *
import cv2 as cv


percentsOfMistakesForClassifiers: list[float] = [0.2, 0.15, 0.1, 0.05, 0.05, 0.05]

maxSizeW = 0
maxSizeH = 0

startSizeW = 200
startSizeH = 200
coef = 1.0
step = 10


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
         x = int(st[0])

         st = lines[i * 5 + 1].split(" ")
         y = int(st[0])

         st = lines[i * 5 + 2].split(" ")
         typeInt = int(st[0])
         type = FeatureType(int(st[0]))

         st = lines[i * 5 + 3].split(" ")
         intency = int(st[0])

         infoArray[int((typeInt + 1)/2)].append(readyFeatureNode(type, x, y, intency))

     return infoArray, size

def checkWindow(matr, x, y, info: list[list[readyFeatureNode]], listNum):
    if (listNum > 5):
        return True

    global coef
    cntMistakes: int = 0

    for node in info[listNum]:
        curFeat = getNode(node.type.value, matr, x + node.x * coef, y + node.y * coef)
        if (curFeat.intensity > node.average * 1.2
            or curFeat.intensity < node.average * 0.8):
            cntMistakes+= 1

    if int(len(info[listNum]) * percentsOfMistakesForClassifiers[listNum]) < cntMistakes:
        return False

    return checkWindow(matr, x, y, info, listNum + 1)

def moving(info, matr):
    global coef
    global startSizeH
    global startSizeW
    global step
    global maxSizeW
    global maxSizeH
    rectList: list[(int, int, int, int)] = []
    x: int = 0
    y: int = 0

    while (startSizeW * coef  < maxSizeW
          and startSizeH * coef < maxSizeH):
        x = 0
        y = 0

        while (x + startSizeW * coef < maxSizeW):
            while(y + startSizeH * coef < maxSizeH):
                if checkWindow(matr, x, y, info, 0):
                    rectList.append((x, y, x + startSizeW * coef, y + startSizeW * coef))
                y += step

            x+=step

        coef += 0.05

    return rectList

def makeRects(image, rectList: list[(int, int, int, int)]):
    for i in rectList:
        image = cv.rectangle(image, (i[0], i[1]), (i[2], i[3]), thickness=2)

def detect(imageName, modelName, maxSize):
    global startSizeW
    global startSizeH
    global maxSizeH
    global maxSizeW
    if maxSize == 300:
        startSizeW = 300

    img = cv.imread(imageName)

    maxSizeH = img.shape[0]
    maxSizeW = img.shape[1]

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    matr = creatingIntegForm(img, startSizeW, startSizeH)
    info = readInfo(modelName)
    moving(info, matr)


