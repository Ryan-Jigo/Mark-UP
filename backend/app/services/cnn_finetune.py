import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# ======================
# Device
# ======================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ======================
# Data augmentation (VERY IMPORTANT for small data)
# ======================
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.Resize((28, 28)),
    transforms.RandomRotation(15),
    transforms.RandomAffine(0, translate=(0.15, 0.15)),
    transforms.RandomPerspective(distortion_scale=0.2, p=0.5),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# ======================
# Load your dataset
# ======================
dataset = datasets.ImageFolder(
    root="dataset",
    transform=transform
)

loader = DataLoader(dataset, batch_size=8, shuffle=True)

print("Classes:", dataset.classes)
print("Total samples:", len(dataset))

# ======================
# CNN Model (same as before)
# ======================
class DigitCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

model = DigitCNN().to(device)

# ======================
# 🔥 Load pretrained MNIST weights
# ======================
model.load_state_dict(torch.load("digit_cnn_mnist.pth", map_location=device))
print("✅ Loaded MNIST pretrained weights")

# ======================
# Loss & optimizer
# ======================
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# ======================
# Fine-tuning loop
# ======================
EPOCHS = 25

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss:.4f}")

print("✅ Fine-tuning completed")

# ======================
# Save new model
# ======================
torch.save(model.state_dict(), "digit_cnn_finetuned.pth")
print("✅ Saved as digit_cnn_finetuned.pth")