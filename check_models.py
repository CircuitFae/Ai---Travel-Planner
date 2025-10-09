import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found. Please set it in your .env file.")
else:
    genai.configure(api_key=api_key)

    print("--- Available Models for Content Generation ---")
    
    # List all available models and filter for the ones that support content generation
    for model in genai.list_models():
      if 'generateContent' in model.supported_generation_methods:
        print(model.name)
        
    print("---------------------------------------------")
    print("\nACTION: Copy one of the model names above (e.g., 'models/gemini-1.0-pro') and update the `genai.GenerativeModel()` line in your main.py file.")