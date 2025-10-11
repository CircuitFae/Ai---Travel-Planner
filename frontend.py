import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# --- Dynamic Backend URL Configuration ---
# This robust logic determines the correct backend URL for any environment.
load_dotenv() # Load .env file if it exists (for local development)

# Check if running on Vercel
if "VERCEL_URL" in os.environ:
    # On Vercel, the backend is at a relative path on the same domain
    API_ENDPOINT = "/api/generate-travel-plan"
# Check if an explicit backend URL is provided (for Render, etc.)
elif "BACKEND_URL" in os.environ:
    base_url = os.getenv("BACKEND_URL")
    API_ENDPOINT = f"{base_url}/generate-travel-plan"
# Fallback for local development
else:
    API_ENDPOINT = "http://127.0.0.1:8000/generate-travel-plan"

# --- Streamlit User Interface ---

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 80rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("AI Student Travel Planner 🎓✈️")
st.info("Tell us about your dream trip, and we'll generate a personalized, budget-friendly itinerary with an interactive map!")

col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("🌍 Where do you want to go?", "e.g., Kyoto, Japan")
    budget = st.selectbox("💰 What's your budget?", ["Budget-friendly", "Moderate", "Luxury"])

with col2:
    duration = st.number_input("📅 How many days?", min_value=1, max_value=30, value=7)
    interests = st.multiselect(
        "🎨 What are your interests?",
        ["History", "Art & Culture", "Food", "Nightlife", "Nature & Outdoors", "Shopping", "Technology"],
        ["History", "Food"]
    )

if st.button("✨ Generate My Itinerary"):
    if destination and duration > 0 and interests:
        # CORRECTED: Simplified payload for budget to be more robust.
        payload = {
            "destination": destination,
            "duration": int(duration),
            "budget": budget,
            "interests": [interest.lower() for interest in interests]
        }
        
        with st.spinner("🌍 Packing our bags and crafting your adventure..."):
            try:
                # CORRECTED: Using the single API_ENDPOINT variable and a robust timeout.
                response = requests.post(API_ENDPOINT, json=payload, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    itinerary = data.get("itinerary")
                    locations = data.get("locations")
                    
                    st.success("🚀 Your personalized travel plan is ready!")
                    st.markdown("---")
                    
                    if locations:
                        st.subheader("📍 Interactive Map")
                        df = pd.DataFrame(locations)
                        df.rename(columns={'latitude': 'lat', 'longitude': 'lon'}, inplace=True)
                        st.map(df)

                    st.subheader("📝 Your Itinerary")
                    st.markdown(itinerary)
                else:
                    st.error(f"Oh no! We hit a bump. Error: {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the planner service. Please make sure the backend is running.")
            except requests.exceptions.Timeout:
                st.error("The request timed out. The AI is taking too long to respond. Please try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please fill in all the fields to get your plan.")

