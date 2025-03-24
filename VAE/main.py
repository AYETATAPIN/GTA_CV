import torch.nn as nn
import torch.optim


from myDataLoader import myDataLoader

hidden_dim = 20
cnt_epochs = 100
max_photo = 1000
path_to_photo = ""
path_to_save = 'D:\Documents\Pycharm Projects\VAE'
name_of_model = 'model'

class Vae(nn.Module):
    def __init__(self, hiddenShapes: [int] = None):
        super(Vae, self).__init__()

    


        modules = []
        if hiddenShapes is None:
            hiddenShapes = [32, 64, 128, 256]

        self.encInChannels = 1
        self.encOutChannels = hiddenShapes[-1]


        start = 1
        for outCh in hiddenShapes:
            modules.append(
                nn.Sequential(
                    nn.Conv2d(start, outCh, 3, stride=2, padding=1),
                    nn.ReLU()
                )
            )
            start = outCh

        self.encoder =  nn.Sequential(*modules)
        self.enc_mu = nn.Linear(hiddenShapes[-1] * 4, hidden_dim)
        self.enc_var = nn.Linear(hiddenShapes[-1] * 4, hidden_dim)

        hiddenShapes.reverse()
        hiddenShapes.append(1)

        modules = []
        self.decoder_in = nn.Linear(hidden_dim, hiddenShapes[0]*4)

        for i in range(len(hiddenShapes) - 1):
            modules.append(
                nn.Sequential(
                    nn.ConvTranspose2d(hiddenShapes[i], hiddenShapes[i+1],
                                       kernel_size = 3, stride= 2, padding=1),
                    nn.ReLU()
                )
            )

        self.decoder = nn.Sequential(*modules)


    def encode(self, x):
        z = self.encoder(x)
        return self.enc_mu(z), self.enc_var(z)

    def reparam(self, mu, var):
        std = torch.exp(0.5*var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, var = self.encode(x)
        z = self.reparam(mu, var)
        return self.decode(z)

model = Vae()
optim = torch.optim.Adam(model.parameters())

def myLoss(myx, x, mu, var):
    RecLoss = nn.functional.binary_cross_entropy(myx, x)
    DKL = -0.5 * torch.sum(1 + var - mu.pow(2) - var.exp())

    return RecLoss + DKL

def train():
    loader = myDataLoader(max_photo, path_to_photo)
    img = loader.getNext()
    while img is not None:
        optim.zero_grad()
        myImg, mu, var = model.forward(img)
        losses = myLoss(myImg, img, mu, var)
        losses.backward()
        optim.step()

def mainTrain(epochs):
    model.train()
    for i in range(epochs):
        train()

if __name__ == "__main__":
    mainTrain(cnt_epochs)
    torch.save(model, path_to_save + '\\' + name_of_model + '.pth')
