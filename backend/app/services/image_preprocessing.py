import cv2
import numpy as np
from PIL import Image

STANDARD_WIDTH = 1500

def standardize_image(image_path: str, debug=True):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read")
    h, w = image.shape[:2]
    scale = 1500 / w
    image = cv2.resize(image, (1500, int(h * scale)))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    deskewed = deskew_image(gray)
    deskewed = cv2.resize(
        deskewed,
        None,
        fx=1.8,
        fy=1.8,
        interpolation=cv2.INTER_CUBIC
    )
    _, binary = cv2.threshold(
        deskewed,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    if np.mean(binary) < 127:
        binary = cv2.bitwise_not(binary)
    
    if debug:
        # Convert to PIL Image and display
        pil_image = Image.fromarray(binary)
        pil_image.show()
    
    return binary



def deskew_image(gray):
    thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]
    coords=np.column_stack(np.where(thresh > 0))
    if len(coords)==0:
        print("No foreground detected")
        return gray
    
    angle = cv2.minAreaRect(coords)[-1]
    if angle<-45:
        angle=-(90 + angle)
    else:
        angle=-angle
    print(f"Detected skew angle: {angle:.2f}")

    if abs(angle) < 1.0:
        print("Angle too small, skipping correction")
        return gray
    h, w = gray.shape
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
    rotated = cv2.warpAffine(
        gray, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    print("Skew correction applied")
    return rotated
