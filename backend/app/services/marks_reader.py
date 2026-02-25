import os
import cv2
from app.services.cnn_predict import predict_digit

DIGIT_FOLDER = "data/clean_digits"


def extract_marks():
    print("=== MARKS EXTRACTION STARTED ===")

    results = {}

    # ✅ safety check
    if not os.path.exists(DIGIT_FOLDER):
        print(f"❌ Folder not found: {DIGIT_FOLDER}")
        return results

    digit_files = sorted([
        f for f in os.listdir(DIGIT_FOLDER)
        if f.endswith(".png")
    ])

    print(f"Found {len(digit_files)} digit cells")

    # 🔥 read each cell
    # 🔥 skip first few rows (tune this number)
    MARK_ROW_START = 24   # 🔥 YOU MUST TUNE THIS
    NUM_QUESTIONS = 10

    for idx, file in enumerate(digit_files[MARK_ROW_START:MARK_ROW_START + NUM_QUESTIONS]):
        path = os.path.join(DIGIT_FOLDER, file)
        img = cv2.imread(path)

        if img is None:
            continue

        value = predict_digit(img)

        if value is None:
            continue

        results[f"Q{idx+1}"] = int(value)
    return results
