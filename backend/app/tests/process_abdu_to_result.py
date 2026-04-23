"""Test script to extract marks from abdu.jpeg and write to result.xlsx."""
from pathlib import Path

from app.services.answer_sheet_extractor import extract_to_result_workbook


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    image_path = backend_root / "data" / "samples" / "abdu.jpeg"
    result_workbook_path = backend_root / "data" / "outputs" / "result.xlsx"

    result = extract_to_result_workbook(
        image_path=image_path,
        result_workbook_path=result_workbook_path,
        row_num=1,
    )
    print("Extraction Result:")
    print(f"Status: {result['status']}")
    print(f"Mode: {result['extraction_mode']}")
    print(f"Roll No: {result['roll_no']}")
    print(f"Student Name: {result['student_name']}")
    print(f"Total Marks: {result['total_marks']}")
    print(f"\nQuestion Marks:")
    for qkey, mark in result['question_marks'].items():
        print(f"  {qkey}: {mark}")
    print(f"\nResult file: {result['result_file']}")


if __name__ == "__main__":
    main()
