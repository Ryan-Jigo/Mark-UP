import pytesseract
from app.config import TESSERACT_PATH
from app.services.image_preprocessing import standardize_image
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(img):
    pil_img = Image.fromarray(img)
    return pytesseract.image_to_string(
        pil_img,
        config="--oem 3 --psm 6"
    ).strip()

