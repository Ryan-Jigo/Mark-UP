import cv2
import numpy as np
import os

INPUT_PATH = "data/rois/marks_table.png"
OUTPUT_DIR = "data/marks_cells"

def ensure_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def segment_table():
    ensure_dir()

    image = cv2.imread(INPUT_PATH)
    if image is None:
        raise ValueError("Marks table image not found")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binary image
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        5
    )

    # --- Detect horizontal lines ---
    horizontal_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (40, 1)
    )
    horizontal = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, horizontal_kernel
    )

    # --- Detect vertical lines ---
    vertical_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, 40)
    )
    vertical = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, vertical_kernel
    )

    # Combine grid
    table_grid = cv2.add(horizontal, vertical)

    # Find contours (cells)
    contours, _ = cv2.findContours(
        table_grid,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cell_count = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # --- Filter small noise ---
        if w < 25 or h < 25:
            continue

        # Crop cell
        cell = image[y:y+h, x:x+w]

        save_path = os.path.join(
            OUTPUT_DIR,
            f"cell_{cell_count:04d}.png"
        )

        cv2.imwrite(save_path, cell)
        cell_count += 1

    print(f"✅ Extracted {cell_count} table cells")