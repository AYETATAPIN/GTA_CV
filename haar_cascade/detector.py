from cascade import getNode, isObj
from imageMaking import creatingIntegForm
from readyFeatureNode import readyFeatureNode, Classifier
from featureNode import *
import cv2 as cv
from numpy import sign



percentsOfMistakesForClassifiers: list[float] = [0.5, 0.1, 0.1, 0.1, 0.05]

maxSizeW = 0
maxSizeH = 0

startSizeW = 200
startSizeH = 200
coefx = 1.0
coefy = 1.0
step = 20


def readInfo(filename):
     size: int
     file = open(filename, mode="r")
     lines = file.readlines()
     size = 0
     classifs: list[Classifier] = []
     i = 0
     while i < len(lines):
        st = lines[i].split(";")
        classifs.append(Classifier())
        classifs[size].weight = float(st[0])
        classifs[size].size = int(st[1])
        i += 2

        for j in range(classifs[size].size):
            st = lines[i].split(" ")
            x = float(st[0])
            i += 1

            st = lines[i].split(" ")
            y = float(st[0])
            i += 1

            st = lines[i].split(" ")
            typeInt = int(st[0])
            type = FeatureType(int(st[0]))
            i += 1

            st = lines[i].split(" ")
            intency = int(st[0])
            i += 2

            classifs[size].addNode(readyFeatureNode(type, x, y, intency))

        size += 1

     return classifs


def checkWindow(matr, x1, y1, x2, y2, classifs:list[Classifier]):

    summary = 0
    for cl in classifs:
        summary += isObj(cl, matr, (x1, y1, x2, y2)) * cl.weight

    if summary >= 0:
        return True
    else:
        return False

def moving(classifis, matr):
    global coefx
    global coefy
    coefx = 1
    coefy = 1
    global startSizeH
    global startSizeW
    global step
    global maxSizeW
    global maxSizeH
    rectList: list[(int, int, int, int)] = []
    x: int = 0
    y: int = 0

    while startSizeW * coefx  <= maxSizeW:
        coefy = 1
        while startSizeH * coefy <= maxSizeH:
            x = 0
            y = 0

            while (x + startSizeW * coefx <= maxSizeW):
                y = 0
                while(y + startSizeH * coefy <= maxSizeH):
                    if checkWindow(matr, x, y, x + startSizeW * coefx, y + startSizeH * coefy, classifis):
                        rectList.append((x, y, x + int(startSizeW * coefx), y + int(startSizeH * coefy)))
                    y += step
                x += step

            coefy += 0.2

        coefx += 0.2

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

