import cv2 as cv
from cv2 import Mat


def createImg(fileName):
    img = cv.imread(fileName)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (200, 200), interpolation=cv.INTER_AREA)
    return img

def creatingIntegForm(image, size1, size2):
    newMatrix: list[(int, int)][(int, int)] = []
    for i in range(size1):
        for j in range(size2):
            left: int = 0
            up: int = 0

            if i == 0:
                up = image[i][j]
            else:
                up = image[i][j] + newMatrix[i - 1][j][0]

            if j == 0:
                left = image[i][j]
            else:
                left = image[i][j] + newMatrix[i][j - 1][1]
    return newMatrix
