import pytesseract
from PIL import Image
import cv2

def extract_header_text(header_img):
    gray = cv2.cvtColor(header_img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(
        gray,
        config="--psm 6"
    )
    return text