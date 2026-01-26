from app.services.image_preprocessing import standardize_image
import cv2

img = standardize_image("data/samples/sample_answer_sheet.png")

cv2.imshow("Deskewed Output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
