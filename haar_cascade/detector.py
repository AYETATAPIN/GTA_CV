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
    min_scale = 0.1  # Минимальная пропорция окна от размеров изображения
    max_scale = 1.0  # Максимальная пропорция окна от размеров изображения
    scale_step = 0.1  # Шаг изменения масштаба окна
    aspect_step = 0.1  # Шаг изменения соотношения сторон
    img_height, img_width = matr.shape
    rectList: list[(int, int, int, int)] = []

    scale = min_scale
    while scale <= max_scale:
        base_width = int(img_width * scale)
        base_height = int(img_height * scale)
        
        aspect_ratio = 1.0
        while aspect_ratio >= aspect_step:
            rect_width = int(base_width * aspect_ratio)
            rect_height = base_height
            scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList)
            aspect_ratio -= aspect_step

        aspect_ratio += aspect_step
        while aspect_ratio < 1.0:
            rect_width = base_width
            rect_height = int(base_height * aspect_ratio)
            scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList)
            aspect_ratio += aspect_step
        
        scale += scale_step

    return rectList

def scan_windows(matr, classifis, rect_width, rect_height, img_width, img_height, rectList):
    global step
    
    x = 0
    while x + rect_width <= img_width:
        y = 0
        while y + rect_height <= img_height:
            if checkWindow(matr, x, y, x + rect_width, y + rect_height, classifis):
                rectList.append((x, y, x + rect_width, y + rect_height))
            y += step
        x += step

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

