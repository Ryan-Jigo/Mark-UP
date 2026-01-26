from PIL import Image, ImageDraw, ImageFont

# Create high-resolution white image
img = Image.new("RGB", (1200, 700), color="white")
draw = ImageDraw.Draw(img)

# Try to load a large font (fallback to default)
try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()

text_lines = [
    "STUDENT ANSWER SCRIPT - FACE SHEET",
    "",
    "Student Name : Rahul Kumar",
    "Register No  : 21CS032",
    "Course       : B.Tech Computer Science",
    "Subject      : Data Science",
    "Semester     : V",
    "Total Marks  : 89",
    "",
    "Verified By  : Examination Cell"
]

y = 50
for line in text_lines:
    draw.text((80, y), line, fill="black", font=font)
    y += 45

# Save with good quality
img.save("data/samples/sample_answer_sheet.png", dpi=(300, 300))

print("High-quality sample image created!")
