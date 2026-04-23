"""Test script to extract marks from multiple answer scripts and populate result.xlsx."""
from pathlib import Path

from app.services.answer_sheet_extractor import extract_to_result_workbook


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    result_workbook_path = backend_root / "data" / "outputs" / "result.xlsx"
    samples_dir = backend_root / "data" / "samples"
    
    # Get all sample images
    sample_images = sorted(samples_dir.glob("*.jpeg"))
    
    print(f"Found {len(sample_images)} sample images")
    print(f"Processing and writing to: {result_workbook_path}\n")
    
    for row_num, image_path in enumerate(sample_images, start=1):
        print(f"Row {row_num}: Processing {image_path.name}...")
        
        result = extract_to_result_workbook(
            image_path=image_path,
            result_workbook_path=result_workbook_path,
            row_num=row_num,
        )
        
        print(f"  Status: {result['status']}")
        print(f"  Mode: {result['extraction_mode']}")
        print(f"  Roll No: {result['roll_no']}")
        print(f"  Student Name: {result['student_name']}")
        print(f"  Total Marks: {result['total_marks']}\n")
    
    print(f"✅ All images processed. Result saved to: {result_workbook_path}")


if __name__ == "__main__":
    main()
