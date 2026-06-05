import os
import sys
import pytesseract
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

# Select Tesseract path dynamically based on platform and environment
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
if not TESSERACT_PATH:
    if sys.platform.startswith("win"):
        TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        # On Linux/macOS, tesseract is typically in the system PATH
        TESSERACT_PATH = "tesseract"

# Only configure tesseract_cmd if it points to a specific executable path (e.g. on Windows or custom path)
if TESSERACT_PATH and TESSERACT_PATH != "tesseract":
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH