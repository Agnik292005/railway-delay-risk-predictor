import streamlit as st
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Railway Delay Risk Predictor",
    layout="centered"
)

st.title("🚆 Railway Delay Risk Predictor")
st.write("Predict whether a train is likely to be delayed based on conditions.")

# ---------------- User Inputs ----------------
distance_km = st.number_input(
    "Distance Between Stations (km)",
    min_value=1,
    max_value=1000,
    value=100
)

weather = st.selectbox(
    "Weather Conditions",
    ["Clear", "Rainy", "Foggy"]
)

day_of_week = st.selectbox(
    "Day of the Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

time_of_day = st.selectbox(
    "Time of Day",
    ["Morning", "Afternoon", "Evening", "Night"]
)

train_type = st.selectbox(
    "Train Type",
    ["Express", "Superfast", "Local"]
)

route_congestion = st.selectbox(
    "Route Congestion",
    ["Low", "Medium", "High"]
)

# ---------------- Prediction ----------------
if st.button("Predict Delay Risk"):
    payload = {
        "distance_km": distance_km,
        "weather": weather,
        "day_of_week": day_of_week,
        "time_of_day": time_of_day,
        "train_type": train_type,
        "route_congestion": route_congestion
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("Prediction Result")
            st.write(f"**Delay Risk:** {result['delay_risk']}")
            st.write(f"**Probability:** {result['probability']}")

        else:
            st.error("Backend error. Please try again.")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend. Is FastAPI running?")

