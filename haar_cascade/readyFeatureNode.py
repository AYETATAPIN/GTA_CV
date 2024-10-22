from featureNode import FeatureType

class readyFeatureNode:
    average = 0
    x: int
    y: int
    type : FeatureType
    isExclusive = True

    def __init__(self, type, x, y, average, isExclusive = True):
        self.average = average
        self.type = type
        self.isExclusive = isExclusive
        self.x = x
        self.y = y

    def setExclusiveness(self, isExclusive):
        self.isExclusive = isExclusive