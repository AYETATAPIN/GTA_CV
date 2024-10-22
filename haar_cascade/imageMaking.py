import cv2 as cv


def createImg(fileName):
    img = cv.imread(fileName)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (200, 200), interpolation=cv.INTER_AREA)
    return img

def creatingIntegForm(image, size1, size2):
    newMatrix: list[list[(int, int, int)]] = []
    endMatrix: list[list[int]] = []
    for i in range(size1):
        newMatrix.append([])
        endMatrix.append([])
        for j in range(size2):
            if i == 0:
                up = int(image[i][j])
            else:
                up = int(image[i][j]) + int(newMatrix[i - 1][j][0])

            if j == 0:
                left = int(image[i][j])
            else:
                left = int(image[i][j]) + int(newMatrix[i][j - 1][1])

            if i == 0:
                if j == 0:
                    all = int(image[i][j])
                else:
                    all = int(image[i][j]) + int(newMatrix[i][j - 1][2])
            else:
                if j == 0:
                    all = int(image[i][j]) + int(newMatrix[i - 1][j][0])
                else:
                    all = int(image[i][j]) + int(newMatrix[i-1][j][0]) + int(newMatrix[i][j-1][2])

            newMatrix[i].append((up, left, all))
            endMatrix[i].append(all)

    return endMatrix
