from enum import Enum

class FeatureType(Enum):
    NOFEATURE = 0
    SIMPLE1 = 1
    SIMPLE2 = 2


class FeatureNode:
    type : FeatureType
    x : int
    y : int
    intensity = 0

    def __init__(self, x, y, type, intensity):
        self.type = FeatureType(type)
        self.x = x
        self.y = y
        self.intensity = intensity

