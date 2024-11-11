from Cython.Tempita.compat3 import coerce_text

from featureNode import FeatureType

cntTypesFeatures = 10

class Feature:
    type: FeatureType

class WeakFeature1(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blacky1: int
    blackx2: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y
        self.blacky2 = y + 4
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 5
        self.whitey2 = y - 1
        self.type = FeatureType.SIMPLE1


    def getIntenceIntegMatrix(self, matrix):

        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        self.intensity = abs(intensityWhite - intensityBlack)
        return abs(intensityWhite - intensityBlack)



class WeakFeature2(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blacky1: int
    blackx2: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.blackx1 = x
        self.blackx2 = x + 4
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.whitex1 = x - 5
        self.whitex2 = x - 1
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.type = FeatureType.SIMPLE2

    def getIntensityIntegMatrix(self, matrix):

        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        self.intensity = abs(intensityWhite - intensityBlack)
        return abs(intensityWhite - intensityBlack)


# “рехполосный горизонтальный признак ’аара
# Ётот признак состоит из трех горизонтальных полос: верхн€€ бела€, средн€€ черна€ и нижн€€ бела€.
class WeakFeature3(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 5
        self.whitey2 = y + 5
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y - 2
        self.blacky2 = y + 2
        self.type = FeatureType.SIMPLE3


    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])
        self.intensity = abs(intensityWhite - intensityBlack * 2)
        return self.intensity




# “рехполосный вертикальный признак ’аара
# Ётот признак состоит из трех вертикальных полос: средн€€ черна€, две боковые белые.
class WeakFeature4(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 5
        self.whitex2 = x + 5
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x - 2
        self.blackx2 = x + 2
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE4



    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])
        self.intensity = abs(intensityWhite - intensityBlack * 2)
        return self.intensity


# „етырехполосный горизонатльный признак ’аара
# Ётот признак состоит из четырех горизонтальных полос: две белые и две черные, чередующиес€ между собой.

class WeakFeature5(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    whitey1_2: int
    whitey2_2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 10
        self.whitey2 = y - 6
        self.whitey1_2 = y + 3
        self.whitey2_2 = y + 7
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y - 10
        self.blacky2 = y + 10
        self.type = FeatureType.SIMPLE5


    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        intensityWhite += matrix[self.whitex2][self.whitey2_2] + matrix[self.whitex1][self.whitey1_2 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1_2 - 1] + matrix[self.whitex1 - 1][self.whitey2_2])

        self.intensity = abs(intensityWhite * 2 - intensityBlack)
        return self.intensity


# „етырехполосный вертикальный признак ’аара
# Ётот признак состоит из четырех вертикальных полос: две белые и две черные, чередующиес€ между собой.
class WeakFeature6(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    whitex1_2: int
    whitex2_2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 10
        self.whitex2 = x - 6
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.whitex1_2 = x
        self.whitex2_2 = x + 4
        self.blackx1 = x - 10
        self.blackx2 = x + 10
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE6

    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        intensityWhite += matrix[self.whitex2_2][self.whitey2] + matrix[self.whitex1_2][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2_2][self.whitey1 - 1] + matrix[self.whitex1_2 - 1][self.whitey2])

        self.intensity = abs(intensityWhite * 2 - intensityBlack)
        return self.intensity


# „етырехугольный признак ’аара
# Ётот признак состоит из четырех квадратов.
class WeakFeature7(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    whitex1_2: int
    whitex2_2: int
    whitey1_2: int
    whitey2_2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 5
        self.whitex2 = x - 1
        self.whitey1 = y - 5
        self.whitey2 = y - 1
        self.whitex1_2 = x
        self.whitex2_2 = x + 4
        self.whitey1_2 = y
        self.whitey2_2 = y + 4
        self.blackx1 = x - 5
        self.blackx2 = x + 4
        self.blacky1 = y - 5
        self.blacky2 = y + 4
        self.type = FeatureType.SIMPLE7

    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        intensityWhite += matrix[self.whitex2_2][self.whitey2] + matrix[self.whitex1_2][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2_2][self.whitey1 - 1] + matrix[self.whitex1_2 - 1][self.whitey2])

        self.intensity = abs(intensityWhite * 2 - intensityBlack)
        return self.intensity


# ѕ€типолосный горизонтальный признак ’аара
# Ётот признак состоит из п€ти горизонтальных полос: три белые полосы чередуютс€ с двум€ черными полосами.

class WeakFeature8(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1_1: int
    whitey2_1: int
    whitey1_2: int
    whitey2_2: int
    whitey1_3: int
    whitey2_3: int
    blackx1: int
    blackx2: int
    blacky1_1: int
    blacky2_1: int
    blacky1_2: int
    blacky2_2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1_1 = y - 10
        self.whitey2_1 = y - 7
        self.whitey1_2 = y - 2
        self.whitey2_2 = y + 1
        self.whitey1_3 = y + 6
        self.whitey2_3 = y + 9
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1_1 = y - 6
        self.blacky2_1 = y - 3
        self.blacky1_2 = y + 2
        self.blacky2_2 = y + 5
        self.type = FeatureType.SIMPLE8



    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2_1] + matrix[self.blackx1][self.blacky1_1 - 1]
        intensityBlack -= matrix[self.blackx2][self.blacky1_1 - 1] + matrix[self.blackx1 - 1][self.blacky2_1]
        intensityBlack += matrix[self.blackx2][self.blacky2_2] + matrix[self.blackx1][self.blacky1_2 - 1]
        intensityBlack -= matrix[self.blackx2][self.blacky1_2 - 1] + matrix[self.blackx1 - 1][self.blacky2_2]

        intensityWhite = matrix[self.whitex2][self.whitey2_3] + matrix[self.whitex1][self.whitey1_3 - 1]
        intensityWhite -= matrix[self.whitex2][self.whitey1_3 - 1] + matrix[self.whitex1 - 1][self.whitey2_3]
        intensityWhite += matrix[self.whitex2][self.whitey2_2] + matrix[self.whitex1][self.whitey1_2 - 1]
        intensityWhite -= matrix[self.whitex2][self.whitey1_2 - 1] + matrix[self.whitex1 - 1][self.whitey2_2]
        intensityWhite += matrix[self.whitex2][self.whitey2_1] + matrix[self.whitex1][self.whitey1_1 - 1]
        intensityWhite -= matrix[self.whitex2][self.whitey1_1 - 1] + matrix[self.whitex1 - 1][self.whitey2_1]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity


# ѕ€типолосный вертикальный признак ’аара
# Ётот признак состоит из п€ти вертикальных полос: две крайние белые, одна черна€ в центре и две черные между ними
class WeakFeature9(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    whitex1_2: int
    whitex2_2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 6
        self.whitex2 = x - 3
        self.whitey1 = y - 5
        self.whitey2 = y + 4
        self.whitex1_2 = x + 2
        self.whitex2_2 = x + 5
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y - 5
        self.blacky2 = y + 4
        self.type = FeatureType.SIMPLE9


    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2]
        
        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= matrix[self.whitex2][self.whitey1 - 1] - matrix[self.whitex1 - 1][self.whitey2]

        intensityWhite += matrix[self.whitex2_2][self.whitey2] + matrix[self.whitex1_2][self.whitey1 - 1]
        intensityWhite -= matrix[self.whitex2_2][self.whitey1 - 1] - matrix[self.whitex1_2 - 1][self.whitey2]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity


# Ўирокополстный горизонтальный признак ’аара
# Ётот признак состоит из одной широкой белой полосы слева и черной полосы справа.
class WeakFeature10(Feature):
    coefx: float
    coefy: float
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int
    intensity = 0

    def __init__(self, x, y, coefx, coefy):
        self.coefx = coefx
        self.coefy = coefy
        self.whitex1 = x - 10
        self.whitex2 = x + 4
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x + 5
        self.blackx2 = x + 9
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE10


    def getIntensityIntegMatrix(self, matrix):
        intensityBlack = matrix[self.blackx2][self.blacky2] + matrix[self.blackx1][self.blacky1 - 1]
        intensityBlack -= (matrix[self.blackx2][self.blacky1 - 1] + matrix[self.blackx1 - 1][self.blacky2])

        intensityWhite = matrix[self.whitex2][self.whitey2] + matrix[self.whitex1][self.whitey1 - 1]
        intensityWhite -= (matrix[self.whitex2][self.whitey1 - 1] + matrix[self.whitex1 - 1][self.whitey2])

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity