from readyFeatureNode import readyFeatureNode
from featureNode import *
import cv2 as cv


percentsOfMistakesForClassifiers: list[float] = [0.2, 0.15, 0.1, 0.05, 0.05, 0.05]

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


def detect(imageName, modelName):
    img = cv.imread(imageName)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    info = readInfo(modelName)
