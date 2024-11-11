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


class FeatureNode:
    type : FeatureType
    x : float
    y : float
    intensity = 0

    def __init__(self, x, y, type, intensity):
        self.type = FeatureType(type)
        self.x = x
        self.y = y
        self.intensity = intensity

