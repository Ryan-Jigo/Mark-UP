import cv2
import os

def segment_cells(cleaned_marks_table, save_dir="data/cells"):
    os.makedirs(save_dir, exist_ok=True)

    # Find contours
    contours, _ = cv2.findContours(
        cleaned_marks_table,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cell_id = 0
    cells = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # FILTER: ignore tiny noise
        if w < 20 or h < 20:
            continue

        cell = cleaned_marks_table[y:y+h, x:x+w]
        cells.append((x, y, cell))

    # SORT: top-to-bottom, left-to-right
    cells = sorted(cells, key=lambda b: (b[1], b[0]))

    saved_paths = []

    for x, y, cell in cells:
        path = f"{save_dir}/cell_{cell_id}.png"
        cv2.imwrite(path, cell)
        saved_paths.append(path)
        cell_id += 1

    return saved_paths