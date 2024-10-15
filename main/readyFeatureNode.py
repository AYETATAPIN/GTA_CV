from featureNode import FeatureType

class readyFeatureNode:
    average = 0
    x: int
    y: int
    type : FeatureType
    isExclusive = True

    def __init__(self, type, x, y, average, isEclusive = True):
        self.average = average
        self.type = type
        self.isExclusive = isEclusive
        self.x = x
        self.y = y

    def setEclusiveness(self, isExclusive):
        self.isExclusive = isExclusive