import cv2
import numpy as np
import pytesseract

def detect_marks_secured(image, marks_table_bbox):
    """
    Detect marks secured box using structure below marks table
    """
    h, w = image.shape[:2]
    x, y, mw, mh = marks_table_bbox

    # Search region BELOW marks table
    search_y1 = y + mh
    search_y2 = min(h, int(y + mh + h * 0.2))
    search = image[search_y1:search_y2, :]

    gray = cv2.cvtColor(search, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        31, 7
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    best = None
    best_area = 0

    for cnt in contours:
        cx, cy, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch

        # Marks secured box size heuristic
        if (
            cw > w * 0.25 and
            cw < w * 0.6 and
            ch > 30 and
            ch < 120
        ):
            if area > best_area:
                best_area = area
                best = (cx, cy, cw, ch)

    if best:
        bx, by, bw, bh = best
        return image[
            search_y1 + by : search_y1 + by + bh,
            bx : bx + bw
        ]

    return None

def detect_layout(image):
    if len(image.shape) == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bin_img = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31, 15
    )

    h, w = gray.shape
    regions = {}

    # ---- HEADER (top 25%) ----
    regions["header"] = image[: int(h * 0.25), :]

    # ---- MARKS TABLE ----
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w // 2, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, h // 25))

    h_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, h_kernel)
    v_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, v_kernel)

    grid = cv2.add(h_lines, v_lines)

    contours, _ = cv2.findContours(
        grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    marks_table_bbox = None
    max_area = 0

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        area = cw * ch

        if (
            cw > w * 0.7 and
            ch > h * 0.15 and
            h * 0.25 < y < h * 0.6
        ):
            if area > max_area:
                max_area = area
                marks_table_bbox = (x, y, cw, ch)

    if marks_table_bbox:
        x, y, cw, ch = marks_table_bbox
        regions["marks_table"] = image[y:y+ch, x:x+cw]
        regions["marks_secured"] = detect_marks_secured(image, marks_table_bbox)
    else:
        regions["marks_table"] = None
        regions["marks_secured"] = None

    return regions