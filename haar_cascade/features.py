from featureNode import FeatureType

cntTypesFeatures = 2

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

    intensity = 0

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
        intensityWhite: int = 0
        intensityBlack: int = 0

        for x in range(self.whitex1, self.whitex1 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx1 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]
        self.intensity = abs(intensityWhite - intensityBlack)

        return self.intensity

    def getIntenceIntegMatrix(self, matrix):

        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        self.intensity = abs(intensityWhite - intensityBlack)
        return abs(intensityWhite - intensityBlack)



class WeakFeature2(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blacky1: int
    blackx2: int
    blacky2: int

    intensity = 0

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
        intensityWhite: int = 0
        intensityBlack: int = 0

        for x in range(self.whitex1, self.whitex1 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx1 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]
        self.intensity = abs(intensityWhite - intensityBlack)

        return self.intensity

    def getIntenceIntegMatrix(self, matrix):
        intensityWhite: int = 0
        intensityBlack: int = 0

        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        return abs(intensityWhite - intensityBlack)

