from cascade import getNode, isObj
from imageMaking import creatingIntegForm
from readyFeatureNode import readyFeatureNode, Classifier
from featureNode import *
import cv2 as cv

percentsOfMistakesForClassifiers: list[float] = [0.5, 0.1, 0.1, 0.1, 0.05]
startSizeW = 200
startSizeH = 200
scale_step = 0.1
aspect_step = 0.1
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
    global startSizeH
    global startSizeW
    global scale_step
    global aspect_step
    img_height, img_width = matr.shape
    rectList: list[(int, int, int, int)] = []
    scales = [scale_step * i for i in range(1, int(1 / scale_step) + 1)]
    ratios = [aspect_step * i for i in range(1, int(1 / aspect_step) + 1)]

    for scale in scales:
        base_width = int(img_width * scale)
        base_height = int(img_height * scale)

        for aspect_ratio in ratios:
            rect_width = int(base_width * aspect_ratio)
            rect_height = base_height
            if (rect_height >= startSizeH) and (rect_width >= startSizeW):
                scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList)
                
            if aspect_ratio != 1:
                rect_width = base_width
                rect_height = int(base_height * aspect_ratio)
                if (rect_height >= startSizeH) and (rect_width >= startSizeW):
                    scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList)

    return rectList

def scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList):
    global step
    max_x = img_width - rect_width + 1
    max_y = img_height - rect_height + 1
    for x in range(0, max_x, step):
        for y in range(0, max_y, step):
            if checkWindow(matr, x, y, x + rect_width, y + rect_height, classifis):
                rectList.append((x, y, x + rect_width, y + rect_height))

def makeRects(image, rectList: list[(int, int, int, int)]):
    for i in rectList:
        image = cv.rectangle(image, (i[0], i[1]), (i[2], i[3]), thickness=2, color=(0, 255, 0))

    return image

def detect(imageName):
    maxSizeW = 0
    maxSizeH = 0
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