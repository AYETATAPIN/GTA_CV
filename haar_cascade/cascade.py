import math
import os

from TrainImageInfo import *
from featureNode import FeatureNode
from features import *
from imageMaking import *
from readyFeatureNode import readyFeatureNode

listFeatSize = 0

sizeW = 200
sizeH = 200

step = 5

def getNode(type, matr, x, y):

    match type:
        case 1:
            node = FeatureNode(x, y, type, WeakFeature1(x, y).getIntenceIntegMatrix(matr))
            return node
        case 2:
            node = FeatureNode(x, y, type, WeakFeature2(x, y).getIntensityIntegMatrix(matr))
            return node
        case 3:
            node = FeatureNode(x, y, type, WeakFeature3(x, y).getIntensityIntegMatrix(matr))
            return node
        case 4:
            node = FeatureNode(x, y, type, WeakFeature4(x, y).getIntensityIntegMatrix(matr))
            return node
        case 5:
            node = FeatureNode(x, y, type, WeakFeature5(x, y).getIntensityIntegMatrix(matr))
            return node
        case 6:
            node = FeatureNode(x, y, type, WeakFeature6(x, y).getIntensityIntegMatrix(matr))
            return node
        case 7:
            node = FeatureNode(x, y, type, WeakFeature7(x, y).getIntensityIntegMatrix(matr))
            return node
        case 8:
            node = FeatureNode(x, y, type, WeakFeature8(x, y).getIntensityIntegMatrix(matr))
            return node
        case 9:
            node = FeatureNode(x, y, type, WeakFeature9(x, y).getIntensityIntegMatrix(matr))
            return node
        case 10:
            node = FeatureNode(x, y, type, WeakFeature10(x, y).getIntensityIntegMatrix(matr))
            return node

def getFeaturesInPoint(matr, x, y):
    listOfFeat: list[FeatureNode] = []
    global listFeatSize
    listFeatSize += cntTypesFeatures
    for type in range(1, cntTypesFeatures + 1):
        node = getNode(type, matr, x, y)
        listOfFeat.append(node)
    return listOfFeat

def getImageInfo(img):
    global listFeatSize
    listFeatSize = 0
    imageInfo = TrainImageInfo()



    matr = creatingIntegForm(img, sizeH, sizeW)

    for y in range(20, sizeW - 19, step):
        for x in range(20, sizeH - 19, step):
            imageInfo.addNodes(getFeaturesInPoint(matr, x, y))

    return imageInfo


def getTrueInfo(trueDic):
    infoArray = []
    infoWeakArray = []
    oldDir = os.getcwd()
    os.chdir(trueDic)
    cntImg = sum([len(files) for r, d, files in os.walk(os.getcwd())])
    infoArray.append(cntImg)
    global listFeatSize

    for i in range(1, cntImg + 1):
        fileName = "car" + str(i) + ".jpg"
        print(f"carNumber = {i}\n")
        infoNode = getImageInfo(createImg(fileName, sizeW, sizeH))
        infoWeakArray.append(infoNode)

    infoArray.append(infoWeakArray)

    os.chdir(oldDir)
    return infoArray


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
                intensity = array[j].FeaturesArray[i].intensity
                aver += intensity * intensity

        if maxCnt != 0 :
            aver/=maxCnt
            aver = int(math.sqrt(aver))
        else:
            aver = 0

        newNode = readyFeatureNode(maxType, x, y, aver)
        readyInfoList.append(newNode)

    return readyInfoList


def analyseInfo(trueDic):
    trueInfoArray = getTrueInfo(trueDic)
    trueReadyInfo = getAverageInfo(trueInfoArray[1], trueInfoArray[0])

    if sizeW == 300:
        falseInfoFileName = "wrongInfo300.txt"
    else:
        falseInfoFileName = "wrongInfo200.txt"

    falseReadyInfo = readWrongInfo(falseInfoFileName)
    weakPercent = 0.1

    for i in range(listFeatSize):
        if trueReadyInfo[i].type == falseReadyInfo[i].type:
            if (trueReadyInfo[i].average*(1 + weakPercent) >= falseReadyInfo[i].average
                    >= trueReadyInfo[i].average*(1 - weakPercent)):
                trueReadyInfo[i].setExclusiveness(False)

    return trueReadyInfo


def writeInfo(array: list[readyFeatureNode], fileToWrite):
    file = open(fileToWrite, mode='w')
    global listFeatSize
    for i in range(0, listFeatSize):
        if array[i].isExclusive:
            file.write(f'{array[i].x}\n{array[i].y}\n{int(array[i].type.value)}\n{int(array[i].average)}\n\n')
    file.close()


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

     return infoArray, size

def makeWrongInfo(falseDic, sizeWidth, sizeHeight, fileWithWrongInfo):
    global sizeW
    global sizeH
    sizeW = sizeWidth
    sizeH = sizeHeight
    falseInfoArray = getFalseInfo(falseDic)
    falseReadyInfo = getAverageInfo(falseInfoArray[1], falseInfoArray[0])
    writeInfo(falseReadyInfo, fileWithWrongInfo)

def learn(trueDic, fileToWrite, sizeWidth, sizeHeight):
    global sizeW
    global sizeH
    sizeW = sizeWidth
    sizeH = sizeHeight
    array = analyseInfo(trueDic)
    writeInfo(array, fileToWrite)



