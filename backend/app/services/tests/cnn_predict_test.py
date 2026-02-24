from app.services.cnn_predict import predict_digits
from app.services.marks_formatter import format_marks

print("🚀 Running digit predictions...")

results = predict_digits()

format_marks(results)