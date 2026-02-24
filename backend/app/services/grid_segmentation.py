def segment_table():
    ensure_dir()

    img = cv2.imread(INPUT_PATH)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bw = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_BINARY_INV,
        cv2.THRESH_BINARY,
        21, 10
    )

    # Detect grid
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    h_lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, h_kernel)
    v_lines = cv2.morphologyEx(bw, cv2.MORPH_OPEN, v_kernel)

    grid = cv2.add(h_lines, v_lines)

    contours, _ = cv2.findContours(
        grid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    idx = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # IMPORTANT: size filter prevents letters
        if w < 40 or h < 30:
            continue

        cell = img[y:y+h, x:x+w]
        cv2.imwrite(f"{OUTPUT_DIR}/cell_{idx:03d}.png", cell)
        idx += 1

    print(f"✅ Cells extracted: {idx}")