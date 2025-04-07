import torchvision
from torch.utils.data import Dataset
import os
import torch

class myDataSet(Dataset):
    def __init__(self, dir):
        self.dir = dir
        self.tr = torchvision.transforms.Resize(size=(512, 512))
        self.images = os.listdir(self.dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):

        img = torchvision.io.read_image(self.dir + '\\' + self.images[index])
        img = self.tr(img)
        img = img.to(torch.float16)
        return img
