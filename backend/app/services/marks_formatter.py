def format_marks(predictions):
    print("\n===== MARKS =====\n")

    subtotal = 0

    for i, val in enumerate(predictions[:10], start=1):
        if val is None:
            print(f"Q{i}: -")
        else:
            print(f"Q{i}: {val}")
            subtotal += val

    print("\n------------------")
    print(f"Subtotal: {subtotal}")