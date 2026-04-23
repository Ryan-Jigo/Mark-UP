"""Test script to extract marks from 4 specific answer scripts and populate result.xlsx."""
from pathlib import Path
import os

from app.services.answer_sheet_extractor import extract_to_result_workbook
from app.services.result_workbook_service import get_or_create_result_workbook


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    result_workbook_path = backend_root / "data" / "outputs" / "result.xlsx"
    samples_dir = backend_root / "data" / "samples"
    
    # Delete existing result.xlsx to start fresh (if not locked)
    if result_workbook_path.exists():
        try:
            result_workbook_path.unlink()
        except PermissionError:
            print(f"Note: Could not delete existing {result_workbook_path} (in use), will overwrite rows\n")
    
    # Create fresh result.xlsx
    get_or_create_result_workbook(result_workbook_path)
    
    # Process 4 specific images
    image_names = ["ryan.jpeg", "varun.jpeg", "abdu.jpeg", "soorya.jpeg"]
    
    print(f"Processing {len(image_names)} images")
    print(f"Writing to: {result_workbook_path}\n")
    
    for row_num, image_name in enumerate(image_names, start=1):
        image_path = samples_dir / image_name
        
        if not image_path.exists():
            print(f"❌ Row {row_num}: {image_name} not found")
            continue
        
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
        print(f"  Total Marks: {result['total_marks']}\n")
    
    print(f"✅ All images processed. Result saved to: {result_workbook_path}")


if __name__ == "__main__":
    main()
