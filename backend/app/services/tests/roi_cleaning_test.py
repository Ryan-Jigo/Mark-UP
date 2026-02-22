import cv2
from app.services.roi_cleaning import (
    clean_header_roi,
    clean_marks_table_roi,
    clean_marks_secured_roi
)

image = cv2.imread("data/samples/demo.png")

header = cv2.imread("data/debug/header.png")
marks_table = cv2.imread("data/debug/marks_table.png")
marks_secured =  cv2.imread("data/debug/marks_secured.png")

cv2.imwrite("data/debug/header_clean.png", clean_header_roi(header))
cv2.imwrite("data/debug/marks_table_clean.png", clean_marks_table_roi(marks_table))
cv2.imwrite("data/debug/marks_secured_clean.png", clean_marks_secured_roi(marks_secured))