from featureNode import FeatureNode


class TrainImageInfo:
    weakFeaturesArray: list[FeatureNode] = []
    weakSize: int
    weakSize = 0

    def addWeakNode(self, FeatureNode):
        self.weakSize += 1
        self.weakFeaturesArray.append(FeatureNode)
