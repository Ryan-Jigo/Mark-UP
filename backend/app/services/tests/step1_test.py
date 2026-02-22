from pathlib import Path
from app.services.image_preprocessing import standardize_image
import cv2
from app.services.ocr_service import extract_text

from app.services.layout_detection import detect_layout

print("=== STEP 1: LAYOUT DETECTION TEST ===")

image_path = "data/samples/demo.png"

outputs = detect_layout(image_path)

for name, path in outputs.items():
    print(f"Saved {name} → {path}")

print("✅ Layout detection completed")





