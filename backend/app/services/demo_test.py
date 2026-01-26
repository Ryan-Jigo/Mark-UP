print("=== DEMO SCRIPT STARTED ===")

from app.services.ocr_service import process_image, extract_text

image_path = "data/samples/img.png"
print("Using image:", image_path)

processed_image = process_image(image_path)
print("Image processed successfully")

text = extract_text(processed_image)

print("====== OCR OUTPUT ======")
print(text)
