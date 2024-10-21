from featureNode import FeatureNode


class TrainImageInfo:
    FeaturesArray: list[FeatureNode] = []
    Size: int
    Size = 0

    def addNodes(self, list: [FeatureNode]):
        self.Size += len(list)
        self.FeaturesArray = self.FeaturesArray + list
