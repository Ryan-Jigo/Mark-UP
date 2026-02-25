import cv2
import torch
import numpy as np
from torchvision import transforms
from PIL import Image
import torch.nn as nn

# ================================
# DEVICE
# ================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ================================
# CNN MODEL
# ================================
class DigitCNN(nn.Module):
    def __init__(self):
        super(DigitCNN, self).__init__()

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


# ================================
# LOAD MODEL
# ================================
model = DigitCNN().to(device)

MODEL_PATH = "digit_cnn_finetuned.pth"

try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()
    print("✅ Finetuned model loaded")
except Exception as e:
    print("❌ Model load failed:", e)


# ================================
# TRANSFORM
# ================================
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])


# ================================
# SINGLE DIGIT PREDICTOR
# ================================
def predict_digit(cell_img):
    """
    Predict digit from one table cell.
    Returns:
        int digit OR None if empty
    """

    # 🔹 convert to grayscale
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)

    # 🔹 quick blank check (VERY IMPORTANT)
    # prevents totally white cells from going to CNN
    if np.mean(gray) > 245:
        return None

    # 🔹 convert to PIL
    pil_img = Image.fromarray(gray)

    tensor = transform(pil_img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)
        confidence, pred = torch.max(probs, dim=1)

    confidence = confidence.item()
    pred = pred.item()

    # 🔥 THIS is the working confidence threshold
    if confidence < 0.99:
        return None
    return pred