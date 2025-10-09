import os
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
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

# --- Pydantic Models ---

class TravelRequest(BaseModel):
    destination: str
    duration: int = Field(..., gt=0, description="Duration in days, must be greater than 0")
    budget: str = Field(..., description="e.g., Budget-friendly, Mid-range, Luxury")
    interests: List[str] = Field(..., description="A list of interests, e.g., ['history', 'food', 'nightlife']")

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Travel Planner API"}

@app.post("/generate-travel-plan")
def generate_travel_plan(request: TravelRequest):
    try:
        model = genai.GenerativeModel('models/gemini-pro-latest')

        # **NEW:** Advanced prompt asking for a JSON output
        prompt = f"""
        You are an expert travel planner specializing in creating itineraries for students.
        Your goal is to create a detailed, exciting, and practical travel plan.
        
        Based on the following details:
        - Destination: {request.destination}
        - Duration: {request.duration} days
        - Budget: {request.budget}
        - Interests: {', '.join(request.interests)}

        Please generate a response in a valid JSON format with two keys:
        1. "itinerary": A string containing a detailed, day-by-day itinerary in Markdown format.
        2. "locations": A JSON array of objects. Each object should represent a specific landmark or restaurant mentioned in the itinerary and must have three keys: "name", "latitude", and "longitude".

        Example for a single location object: {{"name": "Eiffel Tower", "latitude": 48.8584, "longitude": 2.2945}}
        
        Ensure the entire output is a single, valid JSON object.
        """

        response = model.generate_content(prompt)
        
        if not response.parts:
            raise ValueError("The AI response was empty or blocked.")

        # **NEW:** Clean and parse the JSON response from the AI
        response_text = response.text.strip().replace("```json", "").replace("```", "")
        response_data = json.loads(response_text)
        
        return response_data

    except Exception as e:
        print(f"An error occurred: {e}") 
        raise HTTPException(status_code=503, detail=f"Failed to generate itinerary from AI service: {e}")