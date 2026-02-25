import os
import cv2
from app.services.cnn_predict import predict_digit

DIGIT_FOLDER = "data/clean_digits"

print("🚀 Running digit predictions...\n")

digit_files = sorted([
    f for f in os.listdir(DIGIT_FOLDER)
    if f.endswith(".png")
])

for file in digit_files:
    path = os.path.join(DIGIT_FOLDER, file)
    img = cv2.imread(path)

    if img is None:
        print(f"{file} → ❌ image load failed")
        continue

    value = predict_digit(img)

    if value is None:
        print(f"{file} → EMPTY")
    else:
        print(f"{file} → Predicted: {value}")

print("\n✅ Prediction completed")