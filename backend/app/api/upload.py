from pathlib import Path
import tempfile
import re
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Query
from fastapi.responses import FileResponse

from app.services.answer_sheet_extractor import (
	extract_answer_sheet,
	extract_to_result_workbook,
	DEFAULT_OUTPUT_DIR,
)


router = APIRouter()


def _safe_stem(value: str) -> str:
	"""Turn arbitrary text into a filesystem-safe token."""
	return re.sub(r"[^A-Za-z0-9_-]", "_", value.strip())


@router.post("/answer-sheet")
async def upload_answer_sheet(file: UploadFile = File(...)):
	if not file.filename:
		raise HTTPException(status_code=400, detail="An image file is required")

	suffix = Path(file.filename).suffix or ".jpg"
	with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
		temp_file.write(await file.read())
		temp_path = Path(temp_file.name)

	try:
		result = extract_answer_sheet(temp_path)
		return result.to_dict()
	finally:
		temp_path.unlink(missing_ok=True)


@router.post("/marks-to-result")
async def upload_marks_to_result(
	file: UploadFile = File(...),
	row_num: int = Query(1, description="Row number in result.xlsx"),
):
	"""Extract marks from answer sheet image and write to result.xlsx."""
	if not file.filename:
		raise HTTPException(status_code=400, detail="An image file is required")

	suffix = Path(file.filename).suffix or ".jpg"
	with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
		temp_file.write(await file.read())
		temp_path = Path(temp_file.name)

	try:
		result = extract_to_result_workbook(temp_path, row_num=row_num)
		return result
	finally:
		temp_path.unlink(missing_ok=True)


@router.post("/batch")
async def upload_batch(
	files: List[UploadFile] = File(...),
	course: str = Form(...),
	batch: str = Form(...),
	date: str = Form(...),
	exam: str = Form(...),
):
	"""
	Accept multiple answer-sheet images along with batch metadata.
	Each image is processed in order; all student rows land in a single
	result workbook named after the batch.
	Returns a JSON summary including the batch_id (used for downloading).
	"""
	if not files:
		raise HTTPException(status_code=400, detail="At least one image file is required")

	# Build a deterministic, filesystem-safe output filename.
	stem = f"{_safe_stem(course)}_{_safe_stem(batch)}_{_safe_stem(exam)}_{_safe_stem(date)}"
	DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
	result_workbook_path = DEFAULT_OUTPUT_DIR / f"{stem}.xlsx"

	# Remove any stale workbook so we start fresh for this batch.
	if result_workbook_path.exists():
		result_workbook_path.unlink()

	students = []
	errors = []

	for row_num, upload_file in enumerate(files, start=1):
		if not upload_file.filename:
			errors.append({"row": row_num, "error": "Empty filename"})
			continue

		suffix = Path(upload_file.filename).suffix or ".jpg"
		with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
			tmp.write(await upload_file.read())
			tmp_path = Path(tmp.name)

		try:
			result = extract_to_result_workbook(
				image_path=tmp_path,
				result_workbook_path=result_workbook_path,
				row_num=row_num,
			)
			students.append({
				"row": row_num,
				"filename": upload_file.filename,
				"roll_no": result.get("roll_no", ""),
				"student_name": result.get("student_name", ""),
				"total_marks": result.get("total_marks", 0),
				"extraction_mode": result.get("extraction_mode", ""),
			})
		except Exception as exc:
			errors.append({"row": row_num, "filename": upload_file.filename, "error": str(exc)})
		finally:
			tmp_path.unlink(missing_ok=True)

	return {
		"batch_id": stem,
		"course": course,
		"batch": batch,
		"date": date,
		"exam": exam,
		"result_file": str(result_workbook_path),
		"student_count": len(students),
		"students": students,
		"errors": errors,
	}


@router.get("/download/{batch_id}")
async def download_result(batch_id: str):
	"""Stream the result Excel file for the given batch_id back to the client."""
	# Sanitise to prevent path traversal
	safe_id = re.sub(r"[^A-Za-z0-9_-]", "", batch_id)
	file_path = DEFAULT_OUTPUT_DIR / f"{safe_id}.xlsx"

	if not file_path.exists():
		raise HTTPException(status_code=404, detail="Result file not found")

	return FileResponse(
		path=str(file_path),
		media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		filename=f"{safe_id}.xlsx",
	)
