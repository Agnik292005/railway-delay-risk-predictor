import streamlit as st
import requests

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Railway Delay Risk Predictor",
    layout="centered"
)

st.title("🚆 Railway Delay Risk Predictor")
st.write("Predict whether a train is likely to be delayed based on operational and environmental conditions.")

# ---------------- Backend URL ----------------
# IMPORTANT: This must be your deployed backend URL
BACKEND_URL = "https://railway-delay-risk-predictor.onrender.com"

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
        with st.spinner("🚀 Waking up backend (first request may take ~30–60 seconds)..."):
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json=payload,
                timeout=90  # VERY IMPORTANT for Render free-tier cold start
            )

        if response.status_code == 200:
            result = response.json()

            st.subheader("📊 Prediction Result")
            st.success(f"Delay Risk: **{result['delay_risk']}**")
            st.info(f"Probability of Delay: **{result['probability']}**")

        else:
            st.error("Backend returned an error.")
            st.code(response.text)

    except requests.exceptions.Timeout:
        st.warning(
            "⏳ Backend is waking up. Please wait a moment and click **Predict Delay Risk** again."
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Unable to connect to backend. Please try again in a few seconds."
        )

    except Exception as e:
        st.error("Unexpected error occurred.")
        st.exception(e)
