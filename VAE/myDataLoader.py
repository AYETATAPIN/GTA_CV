import torch
import torchvision

class myDataLoader:
    def __init__(self, maxImg, path):
        self.count = 0
        self.max = maxImg
        self.path = path


    def getNext(self):
        if self.count >= self.max:
            return None
        else:
            value = torchvision.io.read_image(self.path + str(self.count) + '.jpg')
            self.count += 1
            tr = torchvision.transforms.Resize(size= (512, 256))
            value = tr(value)

            value = value.to(torch.float32)

            value = value.unsqueeze(0)

            return value
