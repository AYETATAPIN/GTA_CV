from featureNode import FeatureType

cntTypesWeakFeatures = 12

class Feature:
    type: FeatureType

# Двухполосный горизонтальный признак Хаара.
# Этот признак состоит из двух горизонтальных областей: верхней белой и нижней черной

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

        intenceWhite += matrix[self.whitex2][self.whitey2][0] - matrix[self.whitex1][self.whitey1][0]
        intenceWhite += matrix[self.whitex2][self.whitey2][1] - matrix[self.whitex1][self.whitey1][1]

        intenceBlack += matrix[self.blackx2][self.blacky2][0] - matrix[self.blackx1][self.blacky1][0]
        intenceBlack += matrix[self.blackx2][self.blacky2][1] - matrix[self.blackx1][self.blacky1][1]

        return abs(intenceWhite - intenceBlack)

# Двухполосный вертикальный признак Хаара
# Этот признак состоит из двух вертикальных областей: левая белая и правая черная.

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

# Трехполосный горизонтальный признак Хаара
# Этот признак состоит из трех горизонтальных полос: верхняя белая, средняя черная и нижняя белая.

class WeakFeature3(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 5
        self.whitey2 = y - 3
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y - 2
        self.blacky2 = y + 1
        self.type = FeatureType.SIMPLE3

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Трехполосный вертикальный признак Хаара
# Этот признак состоит из трех вертикальных полос: средняя черная, две боковые белые.

class WeakFeature4(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x - 6
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x - 5
        self.blackx2 = x - 1
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE4

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Четырехполосный горизонатльный признак Хаара
# Этот признак состоит из четырех вертикальных полос: две белые и две черные, чередующиеся между собой.
    
class WeakFeature5(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 10
        self.whitey2 = y - 6
        self.whitey1_2 = y + 3 
        self.whitey2_2 = y + 7
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y - 5  
        self.blacky2 = y + 2  
        self.type = FeatureType.SIMPLE5

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1_2, self.whitey2_2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1 + 3, self.blacky2 + 3):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Четырехполосный вертикальный признак Хаара
# Этот признак состоит из четырех вертикальных полос: две белые и две черные, чередующиеся между собой.

class WeakFeature6(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x - 6
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x - 5
        self.blackx2 = x - 1
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE6

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Двухполосный диагональный признак Хаара
# Этот признак состоит из двух диагональных областей: одна белая, другая черная.

class WeakFeature7(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1 = y - 10
        self.whitey2 = y - 1
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1 = y
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE7

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Четырехугольный признак Хаара
# Этот признак состоит из четырех квадратов: два верхних — белых, два нижних — черных.

class WeakFeature8(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 5
        self.whitex2 = x - 1
        self.whitey1 = y - 10
        self.whitey2 = y - 6
        self.blackx1 = x
        self.blackx2 = x + 4
        self.blacky1 = y - 5
        self.blacky2 = y - 1
        self.type = FeatureType.SIMPLE8

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity
    
# Пятиполосный горизонтальный признак Хаара 
# Этот признак состоит из пяти горизонтальных полос: три белые полосы чередуются с двумя черными полосами.
    
class WeakFeature9(Feature):
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

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x + 9
        self.whitey1_1 = y - 10  
        self.whitey2_1 = y - 6
        self.whitey1_2 = y - 2   
        self.whitey2_2 = y + 2
        self.whitey1_3 = y + 6  
        self.whitey2_3 = y + 10
        self.blackx1 = x - 10
        self.blackx2 = x + 9
        self.blacky1_1 = y - 5  
        self.blacky2_1 = y - 3
        self.blacky1_2 = y + 3  
        self.blacky2_2 = y + 5
        self.type = FeatureType.SIMPLE9

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1_1, self.whitey2_1 + 1):
                intensityWhite += img[x][y]

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1_2, self.whitey2_2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1_3, self.whitey2_3 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1_1, self.blacky2_1 + 1):
                intensityBlack += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1_2, self.blacky2_2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Пятиполосный вертикальный признак Хаара 
# Этот признак состоит из пяти вертикальных полос: две крайние белые, одна черная в центре и две черные между ними

class WeakFeature10(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 10
        self.whitex2 = x - 6
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x - 5
        self.blackx2 = x - 1
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.blackx1_2 = x + 1
        self.blackx2_2 = x + 5
        self.type = FeatureType.SIMPLE10

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        for x in range(self.blackx1_2, self.blackx2_2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Широкополстный горизонтальный признак Хаара 
# Этот признак состоит из одной широкой белой полосы слева и черной полосы справа.

class WeakFeature11(Feature):
    whitex1: int
    whitex2: int
    whitey1: int
    whitey2: int
    blackx1: int
    blackx2: int
    blacky1: int
    blacky2: int

    intensity = 0

    def __init__(self, x, y):
        self.whitex1 = x - 20
        self.whitex2 = x + 0
        self.whitey1 = y - 10
        self.whitey2 = y + 9
        self.blackx1 = x + 1
        self.blackx2 = x + 19
        self.blacky1 = y - 10
        self.blacky2 = y + 9
        self.type = FeatureType.SIMPLE11

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.whitex1, self.whitex2 + 1):
            for y in range(self.whitey1, self.whitey2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.blackx1, self.blackx2 + 1):
            for y in range(self.blacky1, self.blacky2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity

# Перекрестный признак Хаара
# Этот признак состоит из двух пересекающихся линий: одна белая горизонтальная и одна черная вертикальная.

class WeakFeature12(Feature):
    white_x1: int
    white_x2: int
    white_y1: int
    white_y2: int
    black_x1: int
    black_x2: int
    black_y1: int
    black_y2: int

    intensity = 0

    def __init__(self, x, y):
        self.white_x1 = x - 10
        self.white_x2 = x + 10
        self.white_y1 = y - 1
        self.white_y2 = y + 1
        self.black_x1 = x - 1
        self.black_x2 = x + 1
        self.black_y1 = y - 10
        self.black_y2 = y + 10
        self.type = FeatureType.SIMPLE12

    def getIntensity(self, img):
        intensityWhite = 0
        intensityBlack = 0

        for x in range(self.white_x1, self.white_x2 + 1):
            for y in range(self.white_y1, self.white_y2 + 1):
                intensityWhite += img[x][y]

        for x in range(self.black_x1, self.black_x2 + 1):
            for y in range(self.black_y1, self.black_y2 + 1):
                intensityBlack += img[x][y]

        self.intensity = abs(intensityWhite - intensityBlack)
        return self.intensity
