import cv2
import numpy as np

standard_width=1200

def standardize_image(image_path:str):
    image=cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read")
    height, width = image.shape[:2]
    scale_ratio = standard_width / width
    if width != standard_width:
        aspect_ratio = height / width
        new_height = int(standard_width * aspect_ratio)
        resized_image = cv2.resize(image, (standard_width, new_height))
        return resized_image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe=cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_image=clahe.apply(gray_image)
    image=cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)
    deskewed_img = deskewed_image(image)
    return deskewed_img

def deskewed_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated