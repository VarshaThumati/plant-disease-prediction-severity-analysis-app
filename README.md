# 🌿 Plant Disease Detection, Severity & Progression Analysis

An AI-powered web application that detects plant diseases from leaf images, estimates disease severity, and predicts future progression risk using deep learning.

---

## 🚀 Project Overview

This project provides an end-to-end solution for plant disease detection using image classification. Users can upload or capture a leaf image, and the system will:

* Identify the disease
* Estimate severity percentage
* Predict future progression risk (Low / Medium / High) with percentage

The system is deployed as a **web application** accessible on both desktop and mobile devices.

---

## 🧠 Key Features

* 📸 Upload or capture leaf images
* 🌱 Disease classification using CNN (TFLite model)
* 📊 Severity estimation (percentage-based)
* 📈 Future progression prediction (rule-based logic)
* ⚡ FastAPI backend for real-time inference
* 🌐 React frontend (mobile-friendly UI)
* ☁️ Fully deployed on Render

---

## 🏗️ System Architecture

```
User (Mobile / Web)
        ↓
React Frontend
        ↓
FastAPI Backend
        ↓
TFLite Model (CNN)
        ↓
Prediction Output
```

---

## 🔬 Methodology

1. Image Input (Upload / Camera)
2. Image Preprocessing (Resize to 224×224, normalization)
3. Model Inference using TFLite
4. Disease Classification
5. Severity Estimation (based on prediction confidence)
6. Future Progression Prediction (rule-based logic)
7. Display results on UI

---

## 🧪 Technologies Used

### Frontend

* React.js
* HTML, CSS

### Backend

* FastAPI (Python)

### AI / Model

* Convolutional Neural Network (CNN)
* TensorFlow Lite (TFLite)

### Libraries

* NumPy
* Pillow
* tflite-runtime

### Deployment

* Render (Frontend + Backend)

---

## 📂 Project Structure

```
plant_disease_web/
│
├── frontend/          # React application
│   ├── src/
│   ├── public/
│   └── package.json
│
└── backend/           # FastAPI backend
    ├── main.py
    ├── requirements.txt
    └── model/
        └── plant_model.tflite
```

---

## 📊 Model Details

* Trained using plant leaf image dataset (PlantVillage)
* Converted to **TensorFlow Lite** for fast inference
* Supports multiple crop diseases

---

## ⚙️ Setup Instructions

### 🔹 Clone the repository

```
git clone https://github.com/VarshaThumati/plant-disease-prediction-severity-analysis-app.git
cd plant-disease-prediction-severity-analysis-app
```

---

### 🔹 Backend Setup

```
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### 🔹 Frontend Setup

```
cd frontend
npm install
npm start
```

---

## 🌐 Deployment

* Backend deployed on Render
* Frontend deployed as static site on Render

---

## 📈 Output

The system provides:

* Disease Name
* Confidence Score
* Severity Percentage
* Future Risk Level (Low / Medium / High)

---

## 📸 Screenshots

*Add your project screenshots here (UI, results, mobile view)*

---

## 🔗 Live Demo

https://plant-disease-prediction-severity.onrender.com

---

## 👩‍💻 Author

**Lakshmi Varsha Thumati**

---

## 📚 References

* PlantVillage Dataset
* Deep Learning for Plant Disease Detection
* FastAPI Documentation
* TensorFlow Lite Documentation
