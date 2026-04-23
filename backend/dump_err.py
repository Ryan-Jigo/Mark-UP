import traceback
from pathlib import Path
from app.services.answer_sheet_extractor import extract_to_result_workbook

try:
    extract_to_result_workbook(
        image_path=Path("data/samples/varun.jpeg"),
        result_workbook_path=Path("data/outputs/test_varun.xlsx")
    )
except Exception as e:
    with open("err.log", "w") as f:
        f.write(traceback.format_exc())
