import os
import google.generativeai as genai
import base64

def main():
    genai.configure(api_key="YOUR_API_KEY_HERE")
    
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
