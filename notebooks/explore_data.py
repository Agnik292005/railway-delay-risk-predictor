import pandas as pd
from pathlib import Path

import joblib


# -------- Load Data --------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "train delay data.csv"

df = pd.read_csv(DATA_PATH)

# -------- Create Target Variable --------
# Delay > 5 minutes -> High Risk (1)
# Delay <= 5 minutes -> Low Risk (0)
df["Delay_Risk"] = (df["Historical Delay (min)"] > 5).astype(int)

# -------- Inspect Target --------
print("Delay Risk Preview:")
print(df[["Historical Delay (min)", "Delay_Risk"]].head(10))

print("\nDelay Risk distribution:")
print(df["Delay_Risk"].value_counts())

# -------- Separate Features and Target --------
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

print("\nFeature sample:")
print(X.head())

print("\nTarget sample:")
print(y.head())


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# -------- Feature Types --------
numeric_features = ["Distance Between Stations (km)"]

categorical_features = [
    "Weather Conditions",
    "Day of the Week",
    "Time of Day",
    "Train Type",
    "Route Congestion",
]

# -------- Preprocessing --------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", "passthrough", numeric_features),
    ]
)

# -------- Model --------
model = LogisticRegression(max_iter=1000)

# -------- Pipeline --------
pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("classifier", model),
    ]
)

# -------- Train-Test Split --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------- Train Model --------
pipeline.fit(X_train, y_train)

# -------- Evaluate --------
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)


# -------- Save Model Pipeline --------
MODEL_PATH = BASE_DIR / "backend" / "delay_risk_pipeline.pkl"

joblib.dump(pipeline, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")

# -------- Load and Test Model --------
loaded_pipeline = joblib.load(MODEL_PATH)

sample_input = X.iloc[[0]]  # one sample row
sample_prediction = loaded_pipeline.predict(sample_input)

print("\nSample prediction:", sample_prediction)
