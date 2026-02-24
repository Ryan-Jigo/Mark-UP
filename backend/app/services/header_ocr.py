import cv2
import pytesseract
from app.config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_header_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Header image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # light preprocessing
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    _, thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    text = pytesseract.image_to_string(thresh)

    print("\n===== OCR HEADER TEXT =====\n")
    print(text)

    return text