from pathlib import Path

from app.services.answer_sheet_extractor import extract_answer_sheet


def main() -> None:
    backend_root = Path(__file__).resolve().parents[2]
    image_path = backend_root / "data" / "samples" / "varun.jpeg"
    output_path = backend_root / "data" / "outputs" / "varun_extracted.xlsx"

    result = extract_answer_sheet(image_path=image_path, output_path=output_path)
    print(result.to_dict())


if __name__ == "__main__":
    main()