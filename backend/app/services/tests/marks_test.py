from app.services.marks_reader import extract_marks

print("=== MARKS EXTRACTION TEST ===\n")

marks = extract_marks()

print("\n===== MARKS =====")
for k, v in marks.items():
    print(f"{k}: {v}")