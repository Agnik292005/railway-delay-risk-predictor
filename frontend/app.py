import streamlit as st
import requests
import time
import streamlit.components.v1 as components

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Railway Delay Risk Predictor",
    layout="centered"
)

st.title("🚆 Railway Delay Risk Predictor")
st.write(
    "Predict whether a train is likely to be delayed based on "
    "operational and environmental conditions."
)

# ---------------- Backend URL ----------------
BACKEND_URL = "https://railway-delay-risk-predictor.onrender.com"

# ---------------- Browser-based Warmup (CRITICAL FIX) ----------------
if "backend_warmed" not in st.session_state:
    st.session_state.backend_warmed = False

def browser_warmup():
    components.html(
        f"""
        <iframe src="{BACKEND_URL}/health" style="display:none;"></iframe>
        """,
        height=0,
        width=0
    )

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

    # Step 1: Browser-style warmup (ONLY ONCE)
    if not st.session_state.backend_warmed:
        with st.spinner("⏳ Starting backend (first use may take ~1 minute)..."):
            browser_warmup()
            time.sleep(40)  # allow backend to fully boot
            st.session_state.backend_warmed = True

    # Step 2: Predict
    try:
        with st.spinner("📊 Predicting delay risk..."):
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json=payload,
                timeout=120
            )

        if response.status_code == 200:
            result = response.json()

            st.subheader("📈 Prediction Result")
            st.success(f"Delay Risk: **{result['delay_risk']}**")
            st.info(f"Probability of Delay: **{result['probability']}**")

        else:
            st.error("Backend returned an error.")
            st.code(response.text)

    except requests.exceptions.Timeout:
        st.error("Backend is still starting. Please try again in a few seconds.")

    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to backend.")

    except Exception as e:
        st.error("Unexpected error occurred.")
        st.exception(e)
