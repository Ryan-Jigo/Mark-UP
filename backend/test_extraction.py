import asyncio
from pathlib import Path
from app.services.answer_sheet_extractor import extract_to_result_workbook

async def main():
    image_path = Path("data/samples/varun.jpeg")
    out_path = Path("data/outputs/test_varun.xlsx")
    
    if out_path.exists():
        out_path.unlink()
        
    print(f"Extracting {image_path} to {out_path} ...")
    
    try:
        result = extract_to_result_workbook(
            image_path=image_path,
            result_workbook_path=out_path,
            row_num=1
        )
        print("RESULT:")
        for k, v in result.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())
