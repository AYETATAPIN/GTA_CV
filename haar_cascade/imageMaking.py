import cv2 as cv


def createImg(fileName, sizeW, sizeH):
    img = cv.imread(fileName)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return img

def creatingIntegForm(image, size1, size2):
    endMatrix: list[list[int]] = []
    for i in range(size1):
        endMatrix.append([])
        for j in range(size2):
            left = 0
            up = 0

            if i == 0:
                up = 0
            else:
                up = int(endMatrix[i - 1][j])

            if j == 0:
                left = 0
            else:
                left = int(endMatrix[i][j - 1])

            if (i != 0 and j != 0):
                all = up + left + image[i][j] - endMatrix[i-1][j-1]
            else:
                all = up + left + image[i][j]

            endMatrix[i].append(all)

    return endMatrix
