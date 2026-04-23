import cv2
import numpy as np

def detect_layout(image, debug=False):
    """
    Robust layout detection for:
    - Header
    - Marks table
    - Marks secured box

    GUARANTEES keys:
    regions["header"]
    regions["marks_table"]
    regions["marks_secured"]
    """

    h, w = image.shape[:2]

    # ---------- PREPROCESS ----------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    bin_img = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31, 15
    )

    # ---------- 1️⃣ HEADER (POSITION-BASED) ----------
    header_top = 0
    header_bottom = int(0.28 * h)   # tuned for your paper

    header = image[header_top:header_bottom, 0:w]

    # ---------- 2️⃣ MARKS TABLE (GRID-BASED) ----------
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (w // 2, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, h // 20))

    h_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, h_kernel)
    v_lines = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, v_kernel)

    grid = cv2.add(h_lines, v_lines)

    contours, _ = cv2.findContours(
        grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    marks_table = None
    table_box = None

    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)

        if (
            y > header_bottom
            and cw > 0.7 * w
            and ch > 0.15 * h
        ):
            marks_table = image[y:y+ch, x:x+cw]
            table_box = (x, y, cw, ch)
            break

    # SAFETY FALLBACK
    if marks_table is None:
        raise RuntimeError("❌ Marks table not detected")

    # ---------- 3️⃣ MARKS SECURED (RELATIVE TO TABLE) ----------
    x, y, cw, ch = table_box

    ms_top = y + ch + int(0.02 * h)
    ms_bottom = ms_top + int(0.10 * h)
    ms_left = int(0.45 * w)
    ms_right = int(0.95 * w)

    marks_secured = image[ms_top:ms_bottom, ms_left:ms_right]

    regions = {
        "header": header,
        "marks_table": marks_table,
        "marks_secured": marks_secured
    }

    # ---------- DEBUG OUTPUT ----------
    if debug:
        cv2.imwrite("data/debug/header.png", header)
        cv2.imwrite("data/debug/marks_table.png", marks_table)
        cv2.imwrite("data/debug/marks_secured.png", marks_secured)

    return regions