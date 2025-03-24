
import torchvision

class myDataLoader:
    def __init__(self, max, path):
        self.count = 0
        self.max = max
        self.path = path


    def getNext(self):
        if self.count >= self.max:
            return None
        else:
            value = torchvision.io.read_image(self.path + str(self.count) + '.jpg')
            self.count += 1
            value = value.unsqueeze(0)
            return value
