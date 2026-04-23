from pathlib import Path
from PIL import Image
import pytesseract
import cv2

from app.services.roi_cleaning import (
    clean_header_roi,
    clean_marks_table_roi,
    clean_marks_secured_roi
)
from app.services.image_preprocessing import standardize_image
from app.services.ocr_service import extract_text
from app.services.layout_detection import crop_regions, detect_layout

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img_path = r"C:\Users\ryanj\Mark-UP\backend\data\samples\demo.png"
processed = standardize_image(img_path)
print("********Image Processing Completed********\n")
text = extract_text(processed)
print("RAW OCR OUTPUT:")
print(text)
print("\n********OCR Extraction Completed********\n")
regions = detect_layout(processed)
cropped = crop_regions(processed, regions)

print(f"Detected regions: {list(cropped.keys())}")

# 🔽 WRITE DEBUG OUTPUTS HERE
if cropped.get("header") is not None:
    cv2.imwrite("data/debug/header.png", cropped["header"])
    print("✅ Saved header.png")
else:
    print("⚠️  Header region not detected")

if cropped.get("marks_table") is not None:
    cv2.imwrite("data/debug/marks_table.png", cropped["marks_table"])
    print("✅ Saved marks_table.png")
else:
    print("⚠️  Marks table region not detected")

if cropped.get("marks_secured") is not None:
    cv2.imwrite("data/debug/marks_secured.png", cropped["marks_secured"])
    print("✅ Saved marks_secured.png")
else:
    print("⚠️  Marks secured region not detected")

print("✅ Debug layout images saved in data/debug/")
print("********Layout Detection Completed********\n")

if cropped.get("header") is not None:
    header = cv2.imread("data/debug/header.png")
    cv2.imwrite("data/debug/header_clean.png", clean_header_roi(header))
    print("✅ Saved header_clean.png")
else:
    print("⚠️  Skipping header cleaning (region not detected)")

if cropped.get("marks_table") is not None:
    marks_table = cv2.imread("data/debug/marks_table.png")
    cv2.imwrite("data/debug/marks_table_clean.png", clean_marks_table_roi(marks_table))
    print("✅ Saved marks_table_clean.png")
else:
    print("⚠️  Skipping marks_table cleaning (region not detected)")

if cropped.get("marks_secured") is not None:
    marks_secured = cv2.imread("data/debug/marks_secured.png")
    cv2.imwrite("data/debug/marks_secured_clean.png", clean_marks_secured_roi(marks_secured))
    print("✅ Saved marks_secured_clean.png")
else:
    print("⚠️  Skipping marks_secured cleaning (region not detected)")
print("********ROI Cleaning Completed********\n")
