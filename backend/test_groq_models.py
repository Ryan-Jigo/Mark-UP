import os
import google.generativeai as genai

def main():
    genai.configure(api_key="YOUR_API_KEY_HERE")
    for m in genai.list_models():
        print(f"MODEL: {m.name}")

if __name__ == "__main__":
    main()
