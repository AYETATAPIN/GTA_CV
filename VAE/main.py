import torch.nn as nn
import torch.optim


from myDataLoader import myDataLoader

startCh = 3
hidden_dim = 20
cnt_epochs = 1000
max_photo = 1000
path_to_photo = ""
path_to_save = 'D:\Documents\Pycharm Projects\VAE'
name_of_model = 'model'

device = 'gpu' if torch.cuda.is_available() else 'cpu'

class Vae(nn.Module):
    def __init__(self):
        super(Vae, self).__init__()


        self.encInChannels = startCh
        self.encOutChannels = 512



        self.ec1 = nn.Conv2d(3, 32, 3, stride=2, padding=1)
        self.ec1A = nn.ReLU()
        self.ec2 = nn.Conv2d(32, 64, 3, stride=2, padding=1)
        self.ec2A = nn.ReLU()
        self.ec3 = nn.Conv2d(64, 128, 3, stride=2, padding=1)
        self.ec3A = nn.ReLU()
        self.ec4 = nn.Conv2d(128, 256, 3, stride=2, padding=1)
        self.ec4A = nn.ReLU()
        self.ec5 = nn.Conv2d(256, 512, 3, stride=2, padding=1)
        self.ec5A = nn.ReLU()

        self.encFlatten = nn.Flatten(start_dim=1)

        self.enc_mu = nn.Linear(512*16*8, hidden_dim)
        self.enc_var = nn.Linear(512*16*8, hidden_dim)



        self.decoder_in = nn.Linear(hidden_dim, 512*8*16)

        self.dc1 = nn.ConvTranspose2d(512, 256, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.dc1A = nn.ReLU()
        self.dc2 = nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.dc2A = nn.ReLU()
        self.dc3 = nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.dc3A = nn.ReLU()
        self.dc4 = nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.dc4A = nn.ReLU()
        self.dc5 = nn.ConvTranspose2d(32, startCh, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.dc5A = nn.ReLU()



    def encode(self, x):
        x = self.ec1A(self.ec1(x))
        x = self.ec2A(self.ec2(x))
        x = self.ec3A(self.ec3(x))
        x = self.ec4A(self.ec4(x))
        x = self.ec5A(self.ec5(x))
        x = self.encFlatten(x)
        return self.enc_mu(x), self.enc_var(x)

    def reparam(self, mu, var):
        std = torch.exp(0.5 * var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        z = self.decoder_in(z)
        z = z.view(1, self.encOutChannels, 16, 8)
        z = self.dc1A(self.dc1(z))
        z = self.dc2A(self.dc2(z))
        z = self.dc3A(self.dc3(z))
        z = self.dc4A(self.dc4(z))
        z = self.dc5A(self.dc5(z))
        return z

    def forward(self, x):
        mu, var = self.encode(x)
        z = self.reparam(mu, var)
        return self.decode(z), mu, var


model = Vae().to(device)
optim = torch.optim.Adam(model.parameters())


def myLoss(myx, x, mu, var):
    RecLoss = nn.functional.mse_loss(myx, x)
    DKL = -0.5 * torch.sum(1 + var - mu.pow(2) - var.exp())

    return RecLoss + DKL


def train():
    loader = myDataLoader(max_photo, path_to_photo)
    img = loader.getNext().to(device)
    while img is not None:
        optim.zero_grad()
        myImg, mu, var = model.forward(img)
        losses = myLoss(myImg, img, mu, var)
        losses.backward()
        optim.step()
        img = loader.getNext().to(device)


def mainTrain(epochs):
    model.train()
    for i in range(epochs):
        train()


if __name__ == "__main__":
    mainTrain(cnt_epochs)
    torch.save(model, path_to_save + '\\' + name_of_model + '.pth')