import math


from TrainImageInfo import *
from featureNode import FeatureNode
from features import *
from imageMaking import *
from readyFeatureNode import readyFeatureNode, Classifier
from train_data_parser import *

cntForFstLearn = 1
cntTrueImagesMax = 2
cntFalseImagesLearn = 1
cntFalseImagesSupL = 2


images = parse_data(DATASET_DIR)

listFeatSize = 0
curFalseImg = 0



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
    global cntForFstLearn

    info = next(images)
    while not (info is None):
        print(f'[{cntImages}] - {info[1]} - learn')
        bb = info[2]
        image = info[0]
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        cntImages += 1
        infoNode = getImageInfo(image, bb)
        infoTempArray.append(infoNode)

        info = next(images)
        if (cntImages == cntForFstLearn):
            break


    infoArray.append(cntImages)
    infoArray.append(infoTempArray)

    return infoArray


def getNextFalse():
    global curFalseImg
    name = "noCars/" + str(curFalseImg) + ".jpg"
    img = cv.imread(name)
    if img is None:
        return None
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    curFalseImg += 1
    return img

def getFalseInfo():
    infoArray = []
    infoTempArray: list[TrainImageInfo] = []
    cntImages = 0
    img = getNextFalse()
    while img is not None:
        bb = (0, 0, img.shape[0], img.shape[1])

        cntImages += 1
        infoNode = getImageInfo(img, bb)
        infoTempArray.append(infoNode)

        if cntImages == cntFalseImagesLearn:
            break
        else:
            img = getNextFalse()

    infoArray.append(cntImages)
    infoArray.append(infoTempArray)
    return infoArray


def getAverageInfo(array: list[TrainImageInfo], size):
    readyInfoList: list[readyFeatureNode] = []
    global listFeatSize

    for i in range(listFeatSize):
        mini = 10000000
        maxi = 0
        aver = 0
        maxType = 0
        x: float = array[0].FeaturesArray[i].x
        y: float = array[0].FeaturesArray[i].y

        for j in range(size):

            intensity = array[j].FeaturesArray[i].intensity
            maxi = max(maxi, intensity)
            mini = min(mini, intensity)
            aver += intensity


        aver = aver//size

        if (maxi - mini <= 10000):
            newNode = readyFeatureNode(array[0].FeaturesArray[i].type, x, y, aver, 1/float(listFeatSize))
            readyInfoList.append(newNode)


    return readyInfoList


def isObj(classifier: Classifier, img, bb):
    cntMistakes = 0

    for node in classifier.nodes:
        inten = getNode(node.type.value, img, bb[0], bb[1], node.x, node.y).intensity
        if  not(node.average * 0.9 <= inten <= node.average * 1.1):
            cntMistakes += 1


    if cntMistakes <= 0.5 * classifier.size:
        return 1
    else:
        return -1

## Разбить фичи Хаара на классифаеры (по необходимости переписать)
def makeClassifiers(info: list[readyFeatureNode]):
    classifiers: list[Classifier] = []
    for i in range(cntTypesFeatures):
        classifiers.append(Classifier())

    for node in info:
        classifiers[node.type.value - 1].addNode(node)

    return classifiers

def getAns(classifs: list[Classifier], cntTrueImages, cntLearnImages):

    answers: list[list[int]] = []
    for i in range(len(classifs)):
        answers.append([])
        for j in range(cntLearnImages):
            answers[i].append(0)

    images = parse_data(DATASET_DIR)
    info = next(images)
    cntImages = 0
    while info is not None:
        bb = info[2]
        image = info[0]
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        matr = creatingIntegForm(image, image.shape[0], image.shape[1])

        for i in range(len(classifs)):
            ans = isObj(classifs[i], matr, bb)
            answers[i][cntImages] = ans

        cntImages += 1
        if cntTrueImages == cntImages:
            break

        info = next(images)
        if images is None:
            cntTrueImages = cntImages

    global cntFalseImagesSupL
    global curFalseImg
    curFalseImg = 0
    img = getNextFalse()
    cntFalseImages = 0
    while img is not None:
        bb = (0, 0, img.shape[0], img.shape[1])
        matr = creatingIntegForm(img, img.shape[0], img.shape[1])

        for i in range(len(classifs)):
            ans = isObj(classifs[i], matr, bb)
            answers[i][cntImages] = ans

        cntImages += 1
        cntFalseImages += 1

        if cntImages == cntFalseImagesSupL + cntTrueImagesMax:
            break
        else:
            img = getNextFalse()
            if img is None:
                cntFalseImages = cntImages

    return answers, cntTrueImages, cntFalseImages



def analyseInfo():
    global images
    trueInfoArray = getTrueInfo()
    trueReadyInfo = getAverageInfo(trueInfoArray[1], trueInfoArray[0])
    classifs = makeClassifiers(trueReadyInfo)

    global cntTrueImagesMax
    global cntFalseImagesSupL
    cntLearnImages = cntTrueImagesMax + cntFalseImagesSupL

    answers, cntTrueImagesMax, cntFalseImagesSupL = getAns(classifs, cntTrueImagesMax, cntLearnImages)
    cntLearnImages = cntTrueImagesMax + cntFalseImagesSupL

    endClassifier: list[Classifier] = []
    sizeEndClass = 0

    weights = []
    errors = []

    classToIt = {}
    itToClass = {}
    for i in range(len(classifs)):
        classToIt.update({classifs[i]: i})
        itToClass.update({i: classifs[i]})
        errors.append(0)

    for j in range(cntLearnImages):
        weights.append(1 / cntLearnImages)

    for i in range(len(classifs)):

        minError = 2
        minErrorIt = -1

        curIt = 0
        curMinIt = -1
        for cl in classifs:

            images = parse_data(DATASET_DIR)
            error = 0

            for ans in range(cntTrueImagesMax):
                if answers[classToIt[cl]][ans] == -1:
                    error += weights[ans]

            for ans in range(cntFalseImagesSupL):
                if answers[classToIt[cl]][ans + cntTrueImagesMax] == 1:
                    error += weights[ans + cntTrueImagesMax]

            errors[classToIt[cl]] = error

            if minError > error:
                minError = error
                minErrorIt = classToIt[cl]
                curMinIt = curIt

            curIt += 1

        endClassifier.append(classifs.pop(curMinIt))
        endClassifier[sizeEndClass].weight = 1/2 * math.log((1 - errors[minErrorIt])/errors[minErrorIt])
        sizeEndClass += 1

        totalW = 0
        for j in range(cntTrueImagesMax):
            weights[j] *= math.exp(-endClassifier[sizeEndClass-1].weight * answers[minErrorIt][j])
            totalW += weights[j]

        for j in range(cntFalseImagesSupL):
            weights[j] *= math.exp(endClassifier[sizeEndClass-1].weight * answers[minErrorIt][j])
            totalW += weights[j]

        for j in range(cntLearnImages):
            weights[j] /= totalW
            totalW += weights[j]


    return endClassifier




def writeInfo(array: list[Classifier], fileToWrite):
    file = open(fileToWrite, mode='w')
    for cl in array:
        file.write(f'{cl.weight};{cl.size}\n\n')
        for feat in cl.nodes:
            file.write(f'{feat.x}\n{feat.y}\n{int(feat.type.value)}\n{int(feat.average)}\n\n')
    file.close()


def learn(fileToWrite):
    print("Start learning\n")
    classifs = analyseInfo()
    print("Start writing\n")
    writeInfo(classifs, fileToWrite)




