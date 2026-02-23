import torch
import torch.nn as nn
import cv2
import os
import numpy as np
from torchvision import transforms


# ======================
# Device setup
# ======================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# ======================
# Model definition (same as training)
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

# ======================
# Load trained model
# ======================
model = DigitCNN().to(device)
model.load_state_dict(torch.load("digit_cnn_finetuned.pth", map_location=device))
model.eval()

print("✅ Finetuned model loaded")

# ======================
# Transform (same as training normalization)
# ======================
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# ======================
# Empty cell detector
# ======================
def is_cell_empty(img):
    """
    Returns True if the cell is blank.
    Works even with light noise.
    """

    # Step 1 — blur to remove tiny noise
    blur = cv2.GaussianBlur(img, (5,5), 0)

    # Step 2 — invert threshold
    thresh = cv2.threshold(
        blur, 240, 255,
        cv2.THRESH_BINARY_INV
    )[1]

    # Step 3 — count ink pixels
    non_zero = cv2.countNonZero(thresh)

    # 🔥 tuned threshold
    return non_zero < 80


# ======================
# Main prediction function
# ======================
INPUT_DIR = "data/clean_digits"

def predict_digits():
    print("\n🚀 Running digit predictions...\n")

    results = []  # 🔥 store predictions

    if not os.path.exists(INPUT_DIR):
        print("❌ clean_digits folder not found")
        return

    files = sorted(os.listdir(INPUT_DIR))

    for file in files:
        path = os.path.join(INPUT_DIR, file)

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        # ===== Empty check =====
        if is_cell_empty(img):
            results.append(None)
            continue

        # ===== Preprocess =====
        # ===== preprocess =====
        img_resized = cv2.resize(img, (28, 28))
        tensor = transform(img_resized).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor)
            probs = torch.softmax(output, dim=1)
            confidence, pred = torch.max(probs, dim=1)

        confidence = confidence.item()
        pred = pred.item()

        # ===== empty handling =====
        if confidence < 0.99:
            results.append(None)
        else:
            results.append(pred)

        

    return results