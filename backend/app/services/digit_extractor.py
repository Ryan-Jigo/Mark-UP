import cv2
import os
import numpy as np

INPUT_DIR = "data/marks_cells"
OUTPUT_DIR = "data/clean_digits"

MIN_PIXEL_THRESHOLD = 80
DIGIT_SIZE = 28


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_cell_empty(binary_img):
    """Return True if mostly blank."""
    non_zero = cv2.countNonZero(binary_img)
    return non_zero < MIN_PIXEL_THRESHOLD


def get_largest_contour(binary_img):
    contours, _ = cv2.findContours(
        binary_img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    return cv2.boundingRect(largest)


def make_square(img):
    h, w = img.shape
    size = max(h, w)

    square = np.zeros((size, size), dtype=np.uint8)

    x_offset = (size - w) // 2
    y_offset = (size - h) // 2

    square[y_offset:y_offset+h, x_offset:x_offset+w] = img
    return square


def process_cells():
    ensure_output_dir()
    saved_count = 0

    for filename in os.listdir(INPUT_DIR):
        path = os.path.join(INPUT_DIR, filename)

        image = cv2.imread(path)
        if image is None:
            continue

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # Skip empty cells
        if is_cell_empty(thresh):
            continue

        bbox = get_largest_contour(thresh)
        if bbox is None:
            continue

        x, y, w, h = bbox
        digit = thresh[y:y+h, x:x+w]

        digit_square = make_square(digit)
        digit_final = cv2.resize(digit_square, (DIGIT_SIZE, DIGIT_SIZE))

        save_path = os.path.join(
            OUTPUT_DIR,
            f"digit_{saved_count:04d}.png"
        )

        cv2.imwrite(save_path, digit_final)
        saved_count += 1

    print(f"✅ Extracted {saved_count} digits")