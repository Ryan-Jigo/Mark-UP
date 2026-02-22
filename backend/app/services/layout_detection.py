import cv2
import numpy as np
import os

def detect_layout(image):
    h, w = image.shape[:2]

    regions = {
        "header": (
            int(0.05 * w),
            int(0.16 * h),
            int(0.90 * w),
            int(0.16 * h)
        ),
        "marks_table": (
            int(0.05 * w),
            int(0.32 * h),
            int(0.90 * w),
            int(0.25 * h)
        ),
        "marks_secured": (
            int(0.60 * w),
            int(0.49* h),
            int(0.35 * w),
            int(0.06 * h)
        )
    }

    return regions

def debug_layout(image, regions, output_path="data/samples/layout_debug.png"):
    debug_img = image.copy()

    for name, box in regions.items():
        if box is None:
            continue
        x, y, w, h = box
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            debug_img, name, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, debug_img)
    print(f"✅ Layout debug image saved at {output_path}")

def crop_regions(image, regions):
    cropped = {}
    for name, (x, y, w, h) in regions.items():
        cropped[name] = image[y:y+h, x:x+w]
    return cropped