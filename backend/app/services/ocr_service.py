import pytesseract
from app.config import TESSERACT_PATH
import cv2
import numpy as np
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def extract_text(image):
    return pytesseract.image_to_string(image)

def process_image(image_path:str):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(5,5),0)
    _, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    processed_image = Image.fromarray(thresh)
    processed_image.show()
    return processed_image