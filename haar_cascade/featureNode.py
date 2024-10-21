from enum import Enum

class FeatureType(Enum):
    NOFEATURE = 0
    SIMPLE1 = 1
    SIMPLE2 = 2
    SIMPLE3 = 3
    SIMPLE4 = 4
    SIMPLE5 = 5
    SIMPLE6 = 6
    SIMPLE7 = 7
    SIMPLE8 = 8
    SIMPLE9 = 9
    SIMPLE10 = 10
    SIMPLE11 = 11
    SIMPLE12 = 12

class FeatureNode:
    type : FeatureType
    x : int
    y : int
    intency = 0

    def __init__(self, x, y, type, intency):
        self.type = FeatureType(type)
        self.x = x
        self.y = y
        self.intency = intency

