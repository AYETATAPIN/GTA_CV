import math
import os

from TrainImageInfo import *
from featureNode import FeatureNode
from features import *
from imageMaking import *
from readyFeatureNode import readyFeatureNode
from train_data_parser import *


listFeatSize = 0

dictOfFeats = {}

boundingBoxX1 = 0
boundingBoxX2 = 0
boundingBoxY1 = 0
boundingBoxY2 = 0

step = 0.1

def getNode(type, matr, x, y, coefx, coefy):

    match type:
        case 1:
            node = FeatureNode(coefx, coefy, type, WeakFeature1(x, y, coefx, coefy).getIntenceIntegMatrix(matr))
            return node
        case 2:
            node = FeatureNode(coefx, coefy, type, WeakFeature2(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 3:
            node = FeatureNode(coefx, coefy, type, WeakFeature3(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 4:
            node = FeatureNode(coefx, coefy, type, WeakFeature4(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 5:
            node = FeatureNode(coefx, coefy, type, WeakFeature5(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 6:
            node = FeatureNode(coefx, coefy, type, WeakFeature6(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 7:
            node = FeatureNode(coefx, coefy, type, WeakFeature7(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 8:
            node = FeatureNode(coefx, coefy, type, WeakFeature8(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 9:
            node = FeatureNode(coefx, coefy, type, WeakFeature9(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node
        case 10:
            node = FeatureNode(coefx, coefy, type, WeakFeature10(x, y, coefx, coefy).getIntensityIntegMatrix(matr))
            return node

def getFeaturesInPoint(matr, x, y, coefx, coefy):
    listOfFeat: list[FeatureNode] = []
    global listFeatSize
    listFeatSize += cntTypesFeatures
    for type in range(1, cntTypesFeatures + 1):
        node = getNode(type, matr, x, y, coefx, coefy)
        listOfFeat.append(node)
    return listOfFeat

def getImageInfo(img, bb):
    global listFeatSize
    listFeatSize = 0
    imageInfo = TrainImageInfo()
    x1 = bb[0]
    y1 = bb[1]
    x2 = bb[2]
    y2 = bb[3]


    matr = creatingIntegForm(img, img.shape[0], img.shape[1])


    for y in range(2, 9, 1):
        for x in range(2, 9, 1):
            xToFeat = int(x1 + (x2 - x1) /10 * step * x)
            yToFeat = int(y1 + (y2 - y1) / 10 * step * y)
            imageInfo.addNodes(getFeaturesInPoint(matr, xToFeat, yToFeat, x * step, y * step))
    return imageInfo


def getTrueInfo():

    infoArray = []
    infoTempArray = []
    cntImages = 0
    global listFeatSize

    images = parse_data(DATASET_DIR)

    info = next(images)
    while not (info is None):
        print(f'[{cntImages}] - {info[1]} - learn')
        cntImages += 1
        bb = info[2]
        image = info[0]
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        infoNode = getImageInfo(image, bb)
        infoTempArray.append(infoNode)

        info = next(images)

    infoArray.append(cntImages)
    infoArray.append(infoTempArray)

    return infoArray

"""
def getFalseInfo(falseDic):
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir(falseDic)
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)

    for i in range(0, cntImg):
        fileName = "wrongPic" + str(i) + ".jpg"
        print(f"falseNum = {i}")
        image = createImg(fileName, sizeW, sizeH)

        if image is None:
            print(f"No file {fileName}\n")
            exit(1)

        infoNode = getImageInfo(image)
        infoWeakArray.append(infoNode)
    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray

"""


def getAverageInfo(array: list[TrainImageInfo], size):
    readyInfoList: list[readyFeatureNode] = []

    for i in range(listFeatSize):
        aver = 0
        maxType = 0
        x: float = array[0].FeaturesArray[i].x
        y: float = array[0].FeaturesArray[i].y
        """
        type: FeatureType
        dictTypes: dict[FeatureType, int] = {}
        for j in range(size):
            x = array[j].FeaturesArray[i].x
            y = array[j].FeaturesArray[i].y
            type = array[j].FeaturesArray[i].type
            if type in dictTypes.keys():
                cnt = dictTypes[type]
                dictTypes[type] = cnt + 1
                if cnt + 1 > maxCnt:
                    maxCnt = cnt + 1
                    maxType = type
            else:
                dictTypes[type] = 1
                if maxCnt == 0:
                    maxCnt = 1
                    maxType = type
        """

        for j in range(size):

            intensity = array[j].FeaturesArray[i].intensity
            aver += intensity


        aver = aver//size


        newNode = readyFeatureNode(array[0].FeaturesArray[i].type, x, y, aver)
        readyInfoList.append(newNode)

    return readyInfoList


def analyseInfo():
    trueInfoArray = getTrueInfo()
    trueReadyInfo = getAverageInfo(trueInfoArray[1], trueInfoArray[0])
    return trueReadyInfo
"""
    falseReadyInfo = readWrongInfo(falseInfoFileName)
    weakPercent = 0.3

    for i in range(listFeatSize):
        if (trueReadyInfo[i].average*(1 + weakPercent) >= falseReadyInfo[i].average
                >= trueReadyInfo[i].average*(1 - weakPercent)):
            trueReadyInfo[i].setExclusiveness(False)"""





def writeInfo(array: list[readyFeatureNode], fileToWrite):
    file = open(fileToWrite, mode='w')
    global listFeatSize
    for i in range(0, listFeatSize):
        if array[i].isExclusive:
            file.write(f'{array[i].x}\n{array[i].y}\n{int(array[i].type.value)}\n{int(array[i].average)}\n\n')
    file.close()


"""
def readWrongInfo(filename):
     size: int
     infoArray: list[readyFeatureNode] = []
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

         infoArray.append(readyFeatureNode(type, x, y, intency))

     return infoArray

def makeWrongInfo(falseDic, sizeWidth, sizeHeight, fileWithWrongInfo):
    global sizeW
    global sizeH
    sizeW = sizeWidth
    sizeH = sizeHeight
    falseInfoArray = getFalseInfo(falseDic)
    falseReadyInfo = getAverageInfo(falseInfoArray[1], falseInfoArray[0])
    writeInfo(falseReadyInfo, fileWithWrongInfo)
"""

def learn(fileToWrite):
    print("Start learning\n")
    array = analyseInfo()
    print("Start writing\n")
    writeInfo(array, fileToWrite)




