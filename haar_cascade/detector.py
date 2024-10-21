from imageMaking import createImg
from readyFeatureNode import readyFeatureNode
from featureNode import *
import cv2 as cv

def readInfo():
     size: int
     infoArray: list[readyFeatureNode] = []
     file = open("model.txt", mode="r")
     lines = file.readlines()
     size = len(lines) // 5
     for i in range(size):

         st = lines[i*5].split(" ")
         x = int(st[0])

         st = lines[i * 5 + 1].split(" ")
         y = int(st[0])

         st = lines[i * 5 + 2].split(" ")
         type = FeatureType(int(st[0]))

         st = lines[i * 5 + 3].split(" ")
         intency = int(st[0])

         infoArray.append(readyFeatureNode(type, x, y, intency))

     return infoArray, size


def detect(fileName):
    img = cv.imread(fileName)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    info = readInfo()
