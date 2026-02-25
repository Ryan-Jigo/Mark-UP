def generate_report(header_data, predictions):
    print("\n==============================")
    print("      STUDENT DETAILS")
    print("==============================\n")

    print(f"Name of Student: {header_data.get('student_name', 'Not Found')}")
    print(f"Course Name: {header_data.get('course_name', 'Not Found')}")
    print(f"Course Code: {header_data.get('course_code', 'Not Found')}")
    print(f"Exam: {header_data.get('exam_name', 'Not Found')}")

    print("\n==============================")
    print("           MARKS")
    print("==============================\n")

    subtotal = 0

    for i, val in enumerate(predictions[:10], start=1):
        if val is None:
            print(f"Q{i}: -")
        else:
            print(f"Q{i}: {val}")
            subtotal += val

    print("\n------------------------------")
    print(f"Subtotal: {subtotal}")