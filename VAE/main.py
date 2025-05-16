import torch.nn as nn
import torch.optim
import torch.utils.tensorboard as tensorboard
from torch import Tensor
import matplotlib.pyplot as plt
import torchvision

from myDataLoader import myDataSet


'''Image.fromarray from PIL, more Linear between 8192 to 64, torchvision.transforms.v2.ToImage'''


startCh = 1
hidden_dim = 128
cnt_epochs = 40
path_to_photo = "D:\\Documents\\PycharmProjects\\Vae2\\cars\\cars"
path_to_save = 'D:\\Documents\\PycharmProjects\\Vae2\\model2'
name_of_model = 'model2'
is_my_KLD = True
batch_size = 128



device = 'cuda' if torch.cuda.is_available() else 'cpu'

class Vae(nn.Module):
    def __init__(self):
        super(Vae, self).__init__()


        self.encInChannels = startCh
        self.encOutChannels = 8192



        self.ec1 = nn.Conv2d(startCh, 32, 3, stride=2, padding=1)
        self.ec1A = nn.LeakyReLU()
        self.ec2 = nn.Conv2d(32, 64, 3, stride=2, padding=1)
        self.ec2A = nn.LeakyReLU()
        self.ec3 = nn.Conv2d(64, 128, 3, stride=2, padding=1)
        self.ec3A = nn.LeakyReLU()
        self.ec4 = nn.Conv2d(128, 256, 3, stride=2, padding=1)
        self.ec4A = nn.LeakyReLU()
        self.ec5 = nn.Conv2d(256, 512, 3, stride=2, padding=1)
        self.ec5A = nn.LeakyReLU()
        self.ec6 = nn.Conv2d(512, 1024, 3, stride=2, padding=1)
        self.ec6A = nn.LeakyReLU()
        self.ec7 = nn.Conv2d(1024, 2048, 3, stride=2, padding=1)
        self.ec7A = nn.LeakyReLU()
        self.ec8 = nn.Conv2d(2048, 4096, 3, stride=2, padding=1)
        self.ec8A = nn.LeakyReLU()
        self.ec9 = nn.Conv2d(4096, 8192, 3, stride=2, padding=1)
        self.ec9A = nn.LeakyReLU()

        self.encFlatten = nn.Flatten(start_dim=1)

        self.encL1 = nn.Linear(8192, 4096)
        self.encL1A = nn.LeakyReLU()
        self.encL2 = nn.Linear(4096, 2048)
        self.encL2A = nn.LeakyReLU()
        self.encL3 = nn.Linear(2048, 1024)
        self.encL3A = nn.LeakyReLU()
        self.encL4 = nn.Linear(1024, 512)
        self.encL4A = nn.LeakyReLU()
        self.encL5 = nn.Linear(512, 256)
        self.encL5A = nn.LeakyReLU()

        self.enc_mu = nn.Linear(256, hidden_dim)
        self.enc_var = nn.Linear(256, hidden_dim)

        self.decoder_in = nn.Linear(hidden_dim, 256)
        self.decoder_inA = nn.LeakyReLU()
        self.decL1 = nn.Linear(256, 512)
        self.decL1A = nn.LeakyReLU()
        self.decL2 = nn.Linear(512, 1024)
        self.decL2A = nn.LeakyReLU()
        self.decL3 = nn.Linear(1024, 2048)
        self.decL3A = nn.LeakyReLU()
        self.decL4 = nn.Linear(2048, 4096)
        self.decL4A = nn.LeakyReLU()
        self.decL5 = nn.Linear(4096, 8192)
        self.decL5A = nn.LeakyReLU()


        self.dc1 = nn.ConvTranspose2d(8192, 4096, 3, stride=2, padding=1, output_padding=1)
        self.dc1A = nn.LeakyReLU()
        self.dc2 = nn.ConvTranspose2d(4096, 2048, 3, stride=2, padding=1, output_padding=1)
        self.dc2A = nn.LeakyReLU()
        self.dc3 = nn.ConvTranspose2d(2048, 1024, 3, stride=2, padding=1, output_padding=1)
        self.dc3A = nn.LeakyReLU()
        self.dc4 = nn.ConvTranspose2d(1024, 512, 3, stride=2, padding=1, output_padding=1)
        self.dc4A = nn.LeakyReLU()
        self.dc5 = nn.ConvTranspose2d(512, 256, 3, stride=2, padding=1, output_padding=1)
        self.dc5A = nn.LeakyReLU()
        self.dc6 = nn.ConvTranspose2d(256, 128, 3, stride=2, padding=1, output_padding=1)
        self.dc6A = nn.LeakyReLU()
        self.dc7 = nn.ConvTranspose2d(128, 64, 3, stride=2, padding=1, output_padding=1)
        self.dc7A = nn.LeakyReLU()
        self.dc8 = nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1)
        self.dc8A = nn.LeakyReLU()
        self.dc9 = nn.ConvTranspose2d(32, startCh, 3, stride=2, padding=1, output_padding=1)



    def encode(self, x):
        x = self.ec1A(self.ec1(x))
        x = self.ec2A(self.ec2(x))
        x = self.ec3A(self.ec3(x))
        x = self.ec4A(self.ec4(x))
        x = self.ec5A(self.ec5(x))
        x = self.ec6A(self.ec6(x))
        x = self.ec7A(self.ec7(x))
        x = self.ec8A(self.ec8(x))
        x = self.ec9A(self.ec9(x))
        x = self.encFlatten(x)
        x = self.encL1A(self.encL1(x))
        x = self.encL2A(self.encL2(x))
        x = self.encL3A(self.encL3(x))
        x = self.encL4A(self.encL4(x))
        x = self.encL5A(self.encL5(x))
        return self.enc_mu(x), self.enc_var(x)

    def reparam(self, mu, var):
        std = torch.exp(0.5 * var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        z = self.decoder_inA(self.decoder_in(z))
        z = self.decL1A(self.decL1(z))
        z = self.decL2A(self.decL2(z))
        z = self.decL3A(self.decL3(z))
        z = self.decL4A(self.decL4(z))
        z = self.encL5A(self.decL5(z))
        z = z.view(batch_size, self.encOutChannels, 1, 1)
        z = self.dc1A(self.dc1(z))
        z = self.dc2A(self.dc2(z))
        z = self.dc3A(self.dc3(z))
        z = self.dc4A(self.dc4(z))
        z = self.dc5A(self.dc5(z))
        z = self.dc6A(self.dc6(z))
        z = self.dc7A(self.dc7(z))
        z = self.dc8A(self.dc8(z))

        return self.dc9(z)


    def forward(self, x):
        mu, var = self.encode(x)
        z = self.reparam(mu, var)
        return self.decode(z), mu, var


model = Vae().to(device)
optim = torch.optim.SGD(model.parameters())
loader = torch.utils.data.DataLoader(myDataSet(path_to_photo), shuffle=True, batch_size=batch_size)
logger = tensorboard.SummaryWriter(log_dir='logging')
scalar = torch.amp.GradScaler()
tr = torchvision.transforms.Resize(size=(512, 512))


def getLoss(myx, x, mu, var):
    RecLoss = nn.functional.binary_cross_entropy_with_logits(myx, x, reduction="sum")

    if is_my_KLD:
        DKL = -0.5 * torch.sum(1 + var - mu.pow(2) - var.exp())
    else:
        DKL = nn.functional.kl_div(myx, x, reduction="batchmean")

    return RecLoss + DKL


def train(epoch):

    sum_losses: Tensor = torch.zeros(1)
    sum_losses = sum_losses.to(device)
    it = 0
    for img in loader:

        print(f'img num = {it*batch_size} - {(it + 1)*batch_size - 1}')
        it += 1
        optim.zero_grad()
        with torch.amp.autocast(device_type=device, dtype=torch.float16):
            myImg, mu, var = model.forward(img)
            losses = getLoss(myImg, img, mu, var)

        sum_losses += losses
        scalar.scale(losses).backward()
        scalar.step(optim)
        scalar.update()

    torch.save(model.state_dict(), path_to_save + '\\' + name_of_model + 'Epoch' + str(epoch) + '.pt')
    logger.add_scalar('Loss', sum_losses, epoch)



def watchImg():
    global batch_size
    old_batch_size = batch_size
    batch_size = 1

    img = loader.dataset.__getitem__(0)
    with torch.amp.autocast(device_type=device, dtype=torch.float16):
        myImg, mu, var = model.forward(img)

    myImg = torch.sigmoid(myImg)

    img = img.cpu() * 256
    img = img.to(torch.uint8)
    plt.imshow(torch.permute(img, (1, 2, 0)).numpy())
    myImg = myImg[0].cpu() * 256
    myImg = myImg.to(torch.uint8)
    plt.imshow(torch.permute(myImg * 256, (1, 2, 0)).numpy())
    plt.show()

    batch_size = old_batch_size

def loadModel(pathToModel):
    model.load_state_dict(torch.load(pathToModel, weights_only=True))


def getImgInFormat(pathToImg):
    img = torchvision.io.read_image(pathToImg)
    img = tr(img)
    img = img.to(torch.float16)

    img_min, img_max = img.min(), img.max()
    img = (img - img_min) / (img_max - img_min)

    img = img.to(device)
    return img.unsqueeze(0), (img_min, img_max)

def encodeImg(pathToImg):
    global batch_size
    batch_size_prev = batch_size
    batch_size = 1
    img, img_info = getImgInFormat(pathToImg)

    with torch.amp.autocast(device_type=device, dtype=torch.float16):
        mu, var = model.encode(img)

    batch_size = batch_size_prev

    return model.reparam(mu, var), img_info



def decodeImg(encodedImg, img_info: (Tensor, Tensor)):
    global batch_size
    batch_size_prev = batch_size
    batch_size = 1

    with torch.amp.autocast(device_type=device, dtype=torch.float16):
        img = model.decode(encodedImg)
        img = torch.sigmoid(img)

    batch_size = batch_size_prev

    img = img * (img_info[1] - img_info[0])  + img_info[0]

    return img

def showForwardedImg(pathToImg):
    model.eval()
    myImg, info = encodeImg(pathToImg)

    myImg = decodeImg(myImg, img_info=info)

    myImg = myImg.to(torch.uint8)
    plt.imshow(torch.permute(myImg, (1, 2, 0)).numpy())



def mainTrain(epochs):
    model.train()
    for i in range(epochs):
        print(f'epoch == {i}\n')
        train(i)



if __name__ == "__main__":
    print(f'device == {device}\n')
    mainTrain(cnt_epochs)
