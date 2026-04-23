from pathlib import Path

from app.services.answer_sheet_extractor import extract_to_result_workbook
from app.services.result_workbook_service import get_or_create_result_workbook


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    result_workbook_path = backend_root / "data" / "outputs" / "result_debug.xlsx"
    samples_dir = backend_root / "data" / "samples"

    if result_workbook_path.exists():
        result_workbook_path.unlink()

    get_or_create_result_workbook(result_workbook_path)

    image_names = ["ryan.jpeg", "varun.jpeg", "abdu.jpeg", "soorya.jpeg"]

    print(f"Processing {len(image_names)} images")
    print(f"Writing to: {result_workbook_path}\n")

    for row_num, image_name in enumerate(image_names, start=1):
        image_path = samples_dir / image_name
        print(f"Row {row_num}: Processing {image_name}...")

        result = extract_to_result_workbook(
            image_path=image_path,
            result_workbook_path=result_workbook_path,
            row_num=row_num,
        )

        print(f"  Status: {result['status']}")
        print(f"  Mode: {result['extraction_mode']}")
        print(f"  Roll No: {result['roll_no']}")
        print(f"  Student Name: {result['student_name']}")
        print(f"  Total Marks: {result['total_marks']}")

        question_marks = result.get("question_marks", {})
        ordered_keys = [f"Q{i}{p}" for i in range(1, 11) for p in ("a", "b")]
        pairs = [f"{k}:{question_marks.get(k, '')}" for k in ordered_keys]
        print("  Marks:", ", ".join(pairs))
        print()

    print(f"Done. Debug workbook: {result_workbook_path}")


if __name__ == "__main__":
    main()
