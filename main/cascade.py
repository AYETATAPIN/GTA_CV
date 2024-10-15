import cv2 as cv
import os

from TrainImageInfo import *
from featureNode import FeatureNode
from features import *
from readyFeatureNode import readyFeatureNode
from imageMaking import *

cntWeakFeatures = 0

def getWeakNode(type, img, x, y):
    match type:
        case 1:
            node = FeatureNode(x, y, type, WeakFeature1(x, y).getIntens(img))
            return node
        case 2:
            node = FeatureNode(x, y, type, WeakFeature2(x, y).getIntens(img))
            return node

def getMostInteresting(img, x, y):
    newNode = FeatureNode(0, 0, 0, 0)
    for type in range(1, cntTypesWeakFeatures + 1):
        node = getWeakNode(type, img, x, y)
        if newNode.type == 0 or node.intency > newNode.intency:
            newNode = node
    return newNode


def getWeakImageInfo(img):
    imageInfo = TrainImageInfo()

    maxS = 180
    minS = 20
    step = 10
    global cntWeakFeatures
    cntWeakFeatures = int((maxS - minS) / step + 1) * int((maxS - minS) / step + 1)
    cntWeakFeatures = int(cntWeakFeatures)

    for x in range(minS, maxS + 1, step):
        for y in range(minS, maxS + 1, step):
            imageInfo.addWeakNode(getMostInteresting(img, x, y))

    return imageInfo


def getTrueInfo():
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir("trueCars")
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)
    global cntWeakFeatures

    for i in range(1, cntImg + 1):
        fileName = "car" + str(i) + ".jpg"
        infoWeakNode = getWeakImageInfo(createImg(fileName))
        infoWeakArray.append(infoWeakNode)
    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray


def getFalseinfo():
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir("falseCars")
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)
    global cntWeakFeatures

    for i in range(1, cntImg + 1):
        fileName = "car" + str(i) + ".jpg"
        infoWeakNode = getWeakImageInfo(createImg(fileName))
        infoWeakArray.append(infoWeakNode)
    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray


def getAverageWeakInfo(array: list[TrainImageInfo], size):
    readyInfoList: list[readyFeatureNode] = []
    global cntWeakFeatures

    for i in range(cntWeakFeatures):
        aver = 0
        maxCnt = 0
        maxType = 0
        x: int = 0
        y: int = 0
        type: FeatureType
        dictTypes: dict[FeatureType, int] = {}
        for j in range(size):
            x = array[j].weakFeaturesArray[i].x
            y = array[j].weakFeaturesArray[i].y
            type = array[j].weakFeaturesArray[i].type
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

        for j in range(size):
            type = array[j].weakFeaturesArray[i].type
            if type == maxType:
                inten = array[j].weakFeaturesArray[i].intency
                aver += inten

        if maxCnt != 0 :
            aver/=maxCnt
        else:
            aver = 0

        newNode = readyFeatureNode(maxType, x, y, aver)
        readyInfoList.append(newNode)

    return readyInfoList


def analyseInfo():
    trueInfoArray = getTrueInfo()
    falseInfoArray = getFalseinfo()
    trueReadyInfo = getAverageWeakInfo(trueInfoArray[1], trueInfoArray[0])
    falseReadyInfo = getAverageWeakInfo(falseInfoArray[1], falseInfoArray[0])
    weakPercent = 0.1

    for i in range(cntWeakFeatures):
        if trueReadyInfo[i].type == falseReadyInfo[i].type:
            if (trueReadyInfo[i].average*(1+weakPercent) >= falseReadyInfo[i].average
                    and trueReadyInfo[i].average*(1-weakPercent) <= falseReadyInfo[i].average):
                trueReadyInfo[i].setEclusiveness(False)

    return trueReadyInfo


def detect():
    array = analyseInfo()
    for i in range(0, cntWeakFeatures):
        if array[i].isExclusive:
            print(array[i].average)

detect()




