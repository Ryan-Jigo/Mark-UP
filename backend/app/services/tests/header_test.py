from app.services.header_ocr import extract_header_text
from app.services.header_parser import parse_header

image_path = "data/samples/demo.png"  # adjust

text = extract_header_text(image_path)
data = parse_header(text)

print("\n===== PARSED DATA =====\n")

print(f"Name of Student: {data.get('student_name', 'Not Found')}")
print(f"Course Name: {data.get('course_name', 'Not Found')}")