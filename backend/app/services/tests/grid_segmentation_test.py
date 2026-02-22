import cv2
from app.services.grid_segmentation import segment_cells

print("=== GRID SEGMENTATION TEST ===")

image = cv2.imread("data/debug/marks_table_clean.png", cv2.IMREAD_GRAYSCALE)

cells = segment_cells(image)

print(f"Total cells detected: {len(cells)}")
for c in cells:
    print(c)