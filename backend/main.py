from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
import pandas as pd

# ---------- App ----------
app = FastAPI(title="Railway Delay Risk API")

# ---------- Load Model ----------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "delay_risk_pipeline.pkl"

pipeline = joblib.load(MODEL_PATH)

# ---------- Input Schema ----------
class PredictionInput(BaseModel):
    distance_km: float
    weather: str
    day_of_week: str
    time_of_day: str
    train_type: str
    route_congestion: str

# ---------- Routes ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: PredictionInput):
    input_df = pd.DataFrame([{
        "Distance Between Stations (km)": data.distance_km,
        "Weather Conditions": data.weather,
        "Day of the Week": data.day_of_week,
        "Time of Day": data.time_of_day,
        "Train Type": data.train_type,
        "Route Congestion": data.route_congestion,
    }])

    prediction = pipeline.predict(input_df)[0]
    probability = pipeline.predict_proba(input_df)[0][1]

    return {
        "delay_risk": "High" if prediction == 1 else "Low",
        "probability": round(probability, 3)
    }
