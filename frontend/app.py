import streamlit as st
import requests
import time

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

# ---------------- Helper: Wake Backend ----------------
def wake_backend(max_wait_seconds=40):
    """
    Polls /health until backend wakes up or timeout is reached.
    Returns True if backend is ready, False otherwise.
    """
    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        try:
            r = requests.get(f"{BACKEND_URL}/health", timeout=5)
            if r.status_code == 200:
                return True
        except:
            pass

        time.sleep(5)  # wait before retrying

    return False

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

    # Step 1: Wake backend FIRST (this is the key fix)
    with st.spinner("⏳ Waking up backend (may take 2 to 3 minutes on first use)..."):
        backend_ready = wake_backend()

    if not backend_ready:
        st.error(
            "Backend is still waking up.\n\n"
            "Please wait a few seconds and click **Predict Delay Risk** again."
        )
    else:
        # Step 2: Call predict ONLY after backend is awake
        try:
            with st.spinner("📊 Predicting delay risk..."):
                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    json=payload,
                    timeout=30
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
            st.error("Prediction timed out. Please try again.")

        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to backend.")

        except Exception as e:
            st.error("Unexpected error occurred.")
            st.exception(e)
