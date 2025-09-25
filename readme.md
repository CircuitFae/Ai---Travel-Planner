# AI Student Travel Planner 🎓✈️

This is a full-stack web application, built entirely in Python, that generates personalized, budget-friendly travel itineraries for students using Google's Gemini AI. The app provides a detailed, day-by-day plan and visualizes the suggested locations on an interactive map.

---

## Features

- **Personalized Itineraries**: Generates travel plans based on destination, duration, budget, and personal interests.
- **Interactive Map**: Displays all suggested landmarks and restaurants on an interactive map for easy visualization.
- **Student-Focused**: The AI is prompted to suggest budget-friendly activities, affordable food options, and public transportation.
- **Modern Tech Stack**:
    - **Backend API**: Built with **FastAPI** for high performance and automatic data validation.
    - **Frontend UI**: A beautiful and interactive user interface built with **Streamlit**.
    - **AI Integration**: Uses the **Google Gemini (`gemini-1.5-flash`)** model to generate structured JSON data, including geographic coordinates.

---

## How to Run This Project

### Prerequisites
- Python 3.8+
- A Google AI API Key

### Setup Instructions

1.  **Clone the repository** and navigate into the project directory.

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    - Create a new file in the root directory named `.env`.
    - Add your Google AI API key to this file:
      ```
      GOOGLE_API_KEY="YOUR_API_KEY_HERE"
      ```

5.  **Run the application:**
    You need to run the backend and frontend servers in two separate terminals.

    - **Terminal 1: Start the Backend**
      ```bash
      uvicorn main:app --reload
      ```
    - **Terminal 2: Start the Frontend**
      ```bash
      streamlit run frontend.py
      ```

    The Streamlit app should automatically open in your browser.