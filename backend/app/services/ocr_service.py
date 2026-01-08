import pytesseract
from app.config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(image):
    return pytesseract.image_to_string(image)
