# 🚆 Railway Delay Risk Predictor

A full-stack machine learning web application that predicts the risk of train delays based on operational and environmental factors.

## 🔗 Live Demo
- **Frontend:** https://railway-delay-risk-predictor-frontend.onrender.com/  
- **Backend API:** https://railway-delay-risk-predictor.onrender.com/docs  

> Note: The backend is hosted on Render free tier and may take ~3 minutes to wake up on first use.

---

## 🧠 Problem Statement
Train delays are influenced by multiple factors such as distance, weather, congestion, and time of travel.  
This project aims to estimate **delay risk** using a trained machine learning model and expose predictions via a web interface.

---

## ⚙️ Architecture
Streamlit Frontend
↓
FastAPI Backend
↓
ML Model (scikit-learn)


- Frontend handles user input and UX
- Backend exposes prediction API
- Model is trained and loaded dynamically on server startup

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
- Handles backend cold-start gracefully
- Fully deployed and accessible globally

---

## 🚀 Key Learnings

- End-to-end ML deployment
- Frontend–backend separation
- Handling cloud free-tier cold starts
- REST API integration
- Real-world debugging and deployment

---

## 📌 Future Improvements

- Larger, real-world datasets
- Geospatial visualization of routes
- Model explainability (SHAP)
- Real-time weather integration


