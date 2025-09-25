import streamlit as st
import requests
import json

# Define the URL of our FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000/generate-travel-plan"

# --- Streamlit User Interface ---

st.title("AI Travel Planner ✈️")

st.write("Enter your destination and the duration of your trip to get a personalized itinerary.")

# Input fields for the user
destination = st.text_input("Destination", "e.g., Paris, France")
duration = st.number_input("Duration (in days)", min_value=1, max_value=30, value=5)

# Button to generate the plan
if st.button("Generate Itinerary"):
    if destination and duration > 0:
        # Prepare the data to be sent to the backend
        payload = {
            "destination": destination,
            "duration": int(duration)
        }
        
        # Show a spinner while waiting for the response
        with st.spinner("Generating your personalized travel plan... This may take a moment."):
            try:
                # Send a POST request to the backend
                response = requests.post(BACKEND_URL, json=payload)
                
                # Check if the request was successful
                if response.status_code == 200:
                    itinerary = response.json().get("itinerary")
                    st.success("Here is your travel plan!")
                    st.write(itinerary)
                else:
                    st.error(f"Error: Could not generate itinerary. Status code: {response.status_code}")
                    st.error(response.text) # Show the error from the backend

            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend. Is the FastAPI server running?")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a destination and duration.")