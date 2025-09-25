import streamlit as st
import requests
import pandas as pd

# Define the URL of our FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000/generate-travel-plan"

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
            "budget": budget.split(" ")[1],
            "interests": [interest.lower() for interest in interests]
        }
        
        with st.spinner("🌍 Packing our bags and crafting your adventure..."):
            try:
                response = requests.post(BACKEND_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    itinerary = data.get("itinerary")
                    locations = data.get("locations")
                    
                    st.success("🚀 Your personalized travel plan is ready!")
                    st.markdown("---")
                    
                    # **NEW:** Display the map if we have location data
                    if locations:
                        st.subheader("📍 Interactive Map")
                        # Create a Pandas DataFrame
                        df = pd.DataFrame(locations)
                        # Rename columns for st.map()
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