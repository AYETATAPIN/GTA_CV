from sympy import false

from featureNode import FeatureType

class readyFeatureNode:
    average = 0
    x: float
    y: float
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


class Classifier:
    nodes: list[readyFeatureNode]
    size = 0
    weight: float = 0

    def __init__(self):
        self.nodes = []

    def addNode(self, node: readyFeatureNode):
        self.nodes.append(node)
        self.size += 1
