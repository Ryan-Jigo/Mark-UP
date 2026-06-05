import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
    genai.configure(api_key=api_key)
    for m in genai.list_models():
        print(f"MODEL: {m.name}")

if __name__ == "__main__":
    main()
