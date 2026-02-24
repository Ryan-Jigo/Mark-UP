import pytesseract
from PIL import Image
import cv2
import numpy as np
from app.config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text(image):
    """
    image: numpy array OR PIL image
    """
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    return pytesseract.image_to_string(image, config="--psm 6")