import cv2
import pytesseract

from app.services.image_preprocessing import standardize_image
from app.services.layout_detection import detect_layout
from app.services.roi_cleaning import (
    clean_header_roi,
    clean_marks_table_roi,
    clean_marks_secured_roi
)
from app.services.ocr_service import extract_text

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("=== TEST TILL NOW STARTED ===")

# -------------------------------
# STEP 1: Load ORIGINAL image
# -------------------------------
img_path = r"data/samples/d2.jpeg"
original = cv2.imread(img_path)

if original is None:
    raise ValueError("❌ Image not found")

print("✅ Original image loaded")

# -------------------------------
# STEP 2: Layout detection
# -------------------------------
regions = detect_layout(original)

print("Detected regions:", regions.keys())

if regions.get("marks_secured") is None:
    print("❌ marks_secured NOT detected")
else:
    print("✅ marks_secured detected",
          regions["marks_secured"].shape)
    
# Debug: Print region dimensions
print(f"Image shape: {original.shape}")
print(f"Regions found: {list(regions.keys())}")
print(f"Header: {regions.get('header').shape if regions.get('header') is not None else 'None'}")
print(f"Marks table: {regions.get('marks_table').shape if regions.get('marks_table') is not None else 'None'}")
print(f"Marks secured: {regions.get('marks_secured').shape if regions.get('marks_secured') is not None else 'None'}")

# Save only non-empty regions
if regions.get("header") is not None and regions["header"].size > 0:
    cv2.imwrite("data/debug/header.png", regions["header"])
    print("✅ Saved header")
else:
    print("⚠️  Header is None or empty")
    
if regions.get("marks_table") is not None and regions["marks_table"].size > 0:
    cv2.imwrite("data/debug/marks_table.png", regions["marks_table"])
    print("✅ Saved marks_table")
else:
    print("⚠️  Marks table is None or empty")
    
if regions.get("marks_secured") is not None and regions["marks_secured"].size > 0:
    cv2.imwrite("data/debug/marks_secured.png", regions["marks_secured"])
    print("✅ Saved marks_secured")
else:
    print("⚠️  Marks secured is None or empty")

print("✅ Layout detection completed")

# -------------------------------
# STEP 3: ROI Cleaning
# -------------------------------
if regions.get("header") is not None:
    header_clean = clean_header_roi(regions["header"])
    cv2.imwrite("data/debug/header_clean.png", header_clean)
    print("✅ Header cleaned")
else:
    print("⚠️  Skipping header cleaning - region not detected")
    header_clean = None

if regions.get("marks_table") is not None:
    marks_table_clean = clean_marks_table_roi(regions["marks_table"])
    cv2.imwrite("data/debug/marks_table_clean.png", marks_table_clean)
    print("✅ Marks table cleaned")
else:
    print("⚠️  Skipping marks table cleaning - region not detected")
    marks_table_clean = None

if regions.get("marks_secured") is not None:
    marks_secured_clean = clean_marks_secured_roi(regions["marks_secured"])
    cv2.imwrite("data/debug/marks_secured_clean.png", marks_secured_clean)
    print("✅ Marks secured cleaned")
else:
    print("⚠️  Skipping marks secured cleaning - region not detected")
    marks_secured_clean = None

print("✅ ROI cleaning completed")

# -------------------------------
# STEP 4: OCR (example: header)
# -------------------------------
if header_clean is not None:
    header_text = extract_text(header_clean)
    print("\n===== HEADER OCR OUTPUT =====")
    print(header_text)
else:
    print("⚠️  Skipping OCR - header not cleaned")

print("\n=== TEST COMPLETED SUCCESSFULLY ===")
