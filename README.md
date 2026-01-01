# 🚆 Railway Delay Risk Predictor

A full-stack machine learning web application that predicts the risk of train delays based on operational and environmental factors.

## 🔗 Live Demo
- **Frontend:** https://railway-delay-risk-predictor-frontend.onrender.com/  
- **Backend API:** https://railway-delay-risk-predictor.onrender.com/docs  

> **Note:** The backend is hosted on Render free tier and may take ~2–3 minutes to wake up on first use due to cold-start behavior.

---

## 🧠 Problem Statement
Train delays are influenced by multiple factors such as distance, weather, congestion, and time of travel.  
This project estimates **delay risk** using a trained machine learning model and exposes predictions via a web interface.

---

## ⚙️ Architecture
Streamlit Frontend
↓
FastAPI Backend
↓
ML Model (scikit-learn)


- Frontend handles user input and user experience
- Backend exposes REST APIs for prediction
- ML model is trained offline and loaded during backend startup

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **ML:** scikit-learn, pandas
- **Deployment:** Render
- **Language:** Python

---

## 📊 Features

- Predicts **High / Low delay risk**
- Returns probability score
- Frontend handles backend cold-start automatically
- Fully deployed and accessible globally

## 🧊 Cold-Start Handling (Deployment Note)

The backend service is hosted on Render free tier, which may enter sleep mode during inactivity.  
To ensure a smooth user experience, the frontend includes logic to automatically handle backend cold-starts before sending prediction requests.

This avoids immediate failures on first use and ensures reliable predictions once the service is active.

---

## 🚀 Key Learnings

- End-to-end ML deployment
- Frontend–backend separation
- Handling cloud free-tier cold starts
- REST API integration
- Debugging real-world deployment issues

---

## 📌 Future Improvements

- Larger, real-world datasets
- Geospatial visualization of railway routes
- Model explainability (e.g., SHAP)
- Real-time weather data integration

