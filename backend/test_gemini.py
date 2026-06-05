import os
import google.generativeai as genai
import base64
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
    genai.configure(api_key=api_key)
    
    # 1x1 pixel black png
    b64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    image_data = base64.b64decode(b64_image)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content(
        [
            "What is in this image? Reply in JSON format: {'result': ''}",
            {"mime_type": "image/png", "data": image_data}
        ],
        generation_config={
            "response_mime_type": "application/json",
        }
    )
    
    print(response.text)

if __name__ == "__main__":
    main()
