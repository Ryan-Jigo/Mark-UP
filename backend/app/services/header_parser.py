import re

def clean_text(value):
    """Remove extra dots and spaces"""
    value = re.sub(r"[._]+$", "", value)  # remove trailing dots
    return value.strip()


def parse_header(text):
    data = {}

    # =========================
    # Student Name
    # handles ; or : variations
    # =========================
    name_match = re.search(
        r"Name\s*of\s*Student\s*[:;]?\s*(.+)",
        text,
        re.I
    )
    if name_match:
        data["student_name"] = clean_text(name_match.group(1))

    # =========================
    # Course Code
    # =========================
    code_match = re.search(
        r"Course\s*Code\s*[:\-]?\s*([A-Z]{2,}\s*\d+)",
        text,
        re.I
    )
    if code_match:
        data["course_code"] = clean_text(code_match.group(1))

    # =========================
    # Course Name
    # =========================
    cname_match = re.search(
        r"Course\s*Name\s*[:\-]?\s*(.+)",
        text,
        re.I
    )
    if cname_match:
        value = cname_match.group(1)

        # remove trailing garbage like 000...
        value = re.sub(r"\d+.*$", "", value)
        data["course_name"] = clean_text(value)

    # =========================
    # Exam Name
    # =========================
    exam_match = re.search(
        r"Name\s*of\s*Examination\s*[:\-]?\s*(.+)",
        text,
        re.I
    )
    if exam_match:
        data["exam_name"] = clean_text(exam_match.group(1))

    return data