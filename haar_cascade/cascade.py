import math

import cv2 as cv
import os

from TrainImageInfo import *
from featureNode import FeatureNode
from features import *
from readyFeatureNode import readyFeatureNode
from imageMaking import *

listFeatSize = 0

def getWeakNode(type, matr, x, y):

    match type:
        case 1:
            node = FeatureNode(x, y, type, WeakFeature1(x, y).getIntenceIntegMatrix(matr))
            return node
        case 2:
            node = FeatureNode(x, y, type, WeakFeature2(x, y).getIntenceIntegMatrix(matr))
            return node

def getFeaturesInPoint(matr, x, y):
    listOfFeat: list[FeatureNode] = []
    global listFeatSize
    listFeatSize += cntTypesFeatures
    for type in range(1, cntTypesFeatures + 1):
        node = getWeakNode(type, matr, x, y)
        listOfFeat.append(node)
    return listOfFeat


def getImageInfo(img):
    global listFeatSize
    listFeatSize = 0
    imageInfo = TrainImageInfo()

    maxS = 180
    minS = 20
    step = 5

    matr = creatingIntegForm(img, 200, 200)

    for x in range(minS, maxS + 1, step):
        for y in range(minS, maxS + 1, step):
            imageInfo.addNodes(getFeaturesInPoint(matr, x, y))

    return imageInfo


def getTrueInfo(trueDic):
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir(trueDic + "trueCars")
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)
    global listFeatSize

    for i in range(1, cntImg + 1):
        fileName = "car" + str(i) + ".jpg"
        infoNode = getImageInfo(createImg(fileName))
        infoWeakArray.append(infoNode)
    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray


def getFalseinfo(falseDic):
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir(falseDic + "falseCars")
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)

    for i in range(1, cntImg + 1):
        fileName = "car" + str(i) + ".jpg"
        infoNode = getImageInfo(createImg(fileName))
        infoWeakArray.append(infoNode)
    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray


def getAverageInfo(array: list[TrainImageInfo], size):
    readyInfoList: list[readyFeatureNode] = []

    for i in range(listFeatSize):
        aver = 0
        maxCnt = 0
        maxType = 0
        x: int = 0
        y: int = 0
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

        for j in range(size):
            type = array[j].FeaturesArray[i].type
            if type == maxType:
                inten = array[j].FeaturesArray[i].intency
                aver += inten * inten

        if maxCnt != 0 :
            aver/=maxCnt
            aver = int(math.sqrt(aver))
        else:
            aver = 0

        newNode = readyFeatureNode(maxType, x, y, aver)
        readyInfoList.append(newNode)

    return readyInfoList


def analyseInfo(trueDic, falseDic):
    trueInfoArray = getTrueInfo(trueDic)
    falseInfoArray = getFalseinfo(falseDic)
    trueReadyInfo = getAverageInfo(trueInfoArray[1], trueInfoArray[0])
    falseReadyInfo = getAverageInfo(falseInfoArray[1], falseInfoArray[0])
    weakPercent = 0.1

    for i in range(listFeatSize):
        if trueReadyInfo[i].type == falseReadyInfo[i].type:
            if (trueReadyInfo[i].average*(1+weakPercent) >= falseReadyInfo[i].average
                    and trueReadyInfo[i].average*(1-weakPercent) <= falseReadyInfo[i].average):
                trueReadyInfo[i].setEclusiveness(False)

    return trueReadyInfo


def writeInfo(array: list[readyFeatureNode], fileToWrite):
    file = open(fileToWrite, mode='w')
    global listFeatSize
    for i in range(0, listFeatSize):
        if array[i].isExclusive:
            file.write(f'{array[i].x}\n{array[i].y}\n{int(array[i].type.value)}\n{int(array[i].average)}\n\n')
    file.close()



def learn(trueDic, falseDic, fileToWrite):
    array = analyseInfo(trueDic, falseDic)
    writeInfo(array, fileToWrite)




