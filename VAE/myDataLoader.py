import torchvision
from torch.utils.data import Dataset
import os
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class myDataSet(Dataset):
    def __init__(self, dir):
        self.dir = dir
        self.tr = torchvision.transforms.Resize(size=(512, 512))
        self.toGrey = torchvision.transforms.Grayscale(num_output_channels=1)
        self.images = os.listdir(self.dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):

        img = torchvision.io.read_image(self.dir + '\\' + self.images[index])
        img = self.toGrey(img)
        img = self.tr(img)
        img = img.to(torch.float16)

        img_min, img_max = img.min(), img.max()
        img = (img - img_min) / (img_max - img_min)

        img = img.to(device)
        return img
