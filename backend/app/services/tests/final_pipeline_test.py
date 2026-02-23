from app.services.header_ocr import extract_header_text
from app.services.header_parser import parse_header
from app.services.cnn_predict import predict_digits
from app.services.report_generator import generate_report

print("🚀 Running FULL pipeline...\n")

# 🔹 Step 1 — OCR header
image_path = "data/samples/demo.png"  # ← update
text = extract_header_text(image_path)
header_data = parse_header(text)

# 🔹 Step 2 — Marks prediction
predictions = predict_digits()

# 🔹 Step 3 — Final report
generate_report(header_data, predictions)