import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=api_key)

# Create an instance of the FastAPI class
app = FastAPI()

# Pydantic model to define the structure of the request body
class TravelRequest(BaseModel):
    destination: str
    duration: int # Duration in days

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Travel Planner API"}

@app.post("/generate-travel-plan")
def generate_travel_plan(request: TravelRequest):
    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create the prompt for the AI
    prompt = f"Create a detailed day-by-day travel itinerary for a {request.duration}-day trip to {request.destination}. Include suggested activities, landmarks, and food recommendations."

    # Generate content using the model
    response = model.generate_content(prompt)

    # Return the generated text
    return {"itinerary": response.text}
    