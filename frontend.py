import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# --- Dynamic Backend URL Configuration ---
# This is the only section that needs to be changed.
# It makes the app work both on Vercel and your local machine.
if "VERCEL_URL" in os.environ:
    # We are running on Vercel, use the public URL with the /api route
    base_url = f"https://{os.getenv('VERCEL_URL')}"
    BACKEND_URL = f"{base_url}/api/generate-travel-plan"
else:
    # We are running locally, use the localhost address
    load_dotenv()
    BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/generate-travel-plan")

# --- Streamlit User Interface ---
# (The rest of your code remains exactly the same)

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
    budget = st.selectbox("💰 What's your budget?", ["💸 Budget-friendly", " moderate", "💰 Luxury"])

with col2:
    duration = st.number_input("📅 How many days?", min_value=1, max_value=30, value=7)
    interests = st.multiselect(
        "🎨 What are your interests?",
        ["History", "Art & Culture", "Food", "Nightlife", "Nature & Outdoors", "Shopping", "Technology"],
        ["History", "Food"]
    )

if st.button("✨ Generate My Itinerary"):
    if destination and duration > 0 and interests:
        payload = {
            "destination": destination,
            "duration": int(duration),
            "budget": budget.split(" ")[1] if " " in budget else budget,
            "interests": [interest.lower() for interest in interests]
        }
        
        with st.spinner("🌍 Packing our bags and crafting your adventure..."):
            try:
                # We are only changing the timeout value in the line below
                response = requests.post(BACKEND_URL, json=payload, timeout=120)
                
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
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please fill in all the fields to get your plan.")


