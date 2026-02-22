import cv2
from app.services.layout_detection import detect_layout, crop_regions

print("=== LAYOUT DETECTION TEST ===")

image = cv2.imread("data/samples/demo.png")
if image is None:
    raise ValueError("Image not found")

regions = detect_layout(image)
cropped = crop_regions(image, regions)

# 🔽 WRITE DEBUG OUTPUTS HERE
cv2.imwrite("data/debug/header.png", cropped["header"])
cv2.imwrite("data/debug/marks_table.png", cropped["marks_table"])
cv2.imwrite("data/debug/marks_secured.png", cropped["marks_secured"])

print("✅ Debug layout images saved in data/debug/")