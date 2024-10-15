from featureNode import FeatureType

cntTypesWeakFeatures = 2

class Feature:
    type: FeatureType

class WeakFeature1(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blacky1: int
    blackx2: int
    blacky2: int

    intence = 0

    def __init__(self, x, y):
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y
        self.blacky2 = y + 4
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 5
        self.whitey2 = y - 1
        self.type = FeatureType.SIMPLE1


    def getIntens(self, img):
        intenceWhite: int = 0
        intenceBlack: int = 0

        for x in range(self.whitex1, self.whitex1 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intenceWhite += img[x][y]

        for x in range(self.blackx1, self.blackx1 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intenceBlack += img[x][y]
        self.intence = abs(intenceWhite - intenceBlack)

        return self.intence

    def getIntenceIntegMatrix(self, matrix):
        intenceWhite: int = 0
        intenceBlack: int = 0

        intenceBlack += matrix[self.blackx2][self.blacky2][0] - matrix[self.blackx1][self.blacky1][0]
        intenceBlack += matrix[self.blackx2][self.blacky2][1] - matrix[self.blackx1][self.blacky1][1]

        intenceWhite += matrix[self.whitex2][self.whitey2][0] - matrix[self.whitex1][self.whitey1][0]
        intenceWhite += matrix[self.whitex2][self.whitey2][1] - matrix[self.whitex1][self.whitey1][1]

        return abs(intenceWhite - intenceBlack)



class WeakFeature2(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blacky1: int
    blackx2: int
    blacky2: int

    intence = 0

    def __init__(self, x, y):
        self.blackx1 = x
        self.blackx2 = x + 4
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.whitex1 = x - 5
        self.whitex2 = x - 1
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.type = FeatureType.SIMPLE2

    def getIntens(self, img):
        intenceWhite: int = 0
        intenceBlack: int = 0

        for x in range(self.whitex1, self.whitex1 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intenceWhite += img[x][y]

        for x in range(self.blackx1, self.blackx1 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intenceBlack += img[x][y]
        self.intence = abs(intenceWhite - intenceBlack)

        return self.intence


