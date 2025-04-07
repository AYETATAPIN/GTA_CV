import torch.nn as nn
import torch.optim
import torch.utils.tensorboard as tensorboard
from torch import Tensor

from myDataLoader import myDataSet

startCh = 3
hidden_dim = 20
cnt_epochs = 100
path_to_photo = "D:\\Documents\\Pycharm Projects\\Vae2\\cars\\cars"
path_to_save = 'D:\\Documents\\Pycharm Projects\\Vae2'
name_of_model = 'model'
is_my_KLD = False


device = 'gpu' if torch.cuda.is_available() else 'cpu'

class Vae(nn.Module):
    def __init__(self):
        super(Vae, self).__init__()


        self.encInChannels = startCh
        self.encOutChannels = 8192



        self.ec1 = nn.Conv2d(3, 32, 3, stride=2, padding=1)
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

        self.enc_mu = nn.Linear(8192, hidden_dim)
        self.enc_var = nn.Linear(8192, hidden_dim)

        self.decoder_in = nn.Linear(hidden_dim, 8192)
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
        self.dc9A = nn.LeakyReLU()



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
        return self.enc_mu(x), self.enc_var(x)

    def reparam(self, mu, var):
        std = torch.exp(0.5 * var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        z = self.decoder_in(z)
        z = z.view(1, self.encOutChannels, 1, 1)
        z = self.dc1A(self.dc1(z))
        z = self.dc2A(self.dc2(z))
        z = self.dc3A(self.dc3(z))
        z = self.dc4A(self.dc4(z))
        z = self.dc5A(self.dc5(z))
        z = self.dc6A(self.dc6(z))
        z = self.dc7A(self.dc7(z))
        z = self.dc8A(self.dc8(z))
        z = self.dc9A(self.dc9(z))
        return z

    def forward(self, x):
        mu, var = self.encode(x)
        z = self.reparam(mu, var)
        return self.decode(z), mu, var


model = Vae().to(device)
optim = torch.optim.Adam(model.parameters())
loader = torch.utils.data.DataLoader(myDataSet(path_to_photo), shuffle=True)
logger = tensorboard.SummaryWriter(log_dir='logging')

def myLoss(myx, x, mu, var):
    RecLoss = nn.functional.mse_loss(myx, x)

    if is_my_KLD:
        DKL = -0.5 * torch.sum(1 + var - mu.pow(2) - var.exp())
    else:
        DKL = nn.functional.kl_div(myx, x)

    return RecLoss + DKL


def train(epoch):

    sum_losses: Tensor = torch.zeros(1)
    for img in loader:
        optim.zero_grad()
        myImg, mu, var = model.forward(img)
        losses = myLoss(myImg, img, mu, var)
        sum_losses += losses
        losses.backward()
        optim.step()

    logger.add_scalar('Loss', sum_losses, epoch)




def mainTrain(epochs):
    model.train()
    for i in range(epochs):
        print(f'epoch == {i}\n')
        train(i)



if __name__ == "__main__":
    mainTrain(cnt_epochs)
    torch.save(model, path_to_save + '\\' + name_of_model + '.pth')