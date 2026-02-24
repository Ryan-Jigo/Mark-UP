import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open(r"C:\Users\ryanj\Mark-UP\backend\data\samples\image.png")
text = pytesseract.image_to_string(img)

print("RAW OCR OUTPUT:")
print(text)