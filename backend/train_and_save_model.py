from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "train delay data.csv"
MODEL_PATH = Path(__file__).resolve().parent / "delay_risk_pipeline.pkl"

df = pd.read_csv(DATA_PATH)

df["Delay_Risk"] = (df["Historical Delay (min)"] > 5).astype(int)

X = df[
    [
        "Distance Between Stations (km)",
        "Weather Conditions",
        "Day of the Week",
        "Time of Day",
        "Train Type",
        "Route Congestion",
    ]
]

y = df["Delay_Risk"]

numeric_features = ["Distance Between Stations (km)"]
categorical_features = [
    "Weather Conditions",
    "Day of the Week",
    "Time of Day",
    "Train Type",
    "Route Congestion",
]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ]
)

pipeline.fit(X, y)

joblib.dump(pipeline, MODEL_PATH)

print("Model trained and saved successfully")
