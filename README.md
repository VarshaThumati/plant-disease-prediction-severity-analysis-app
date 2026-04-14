# 🌿 Plant Disease Detection, Severity & Progression Analysis

I designed and developed a full-stack web application along with a custom AI model, built independently as a separate project, to detect plant diseases from leaf images, estimate severity, and predict future progression using deep learning.

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

Unhealthy Leaf Analysis

<img width="1916" height="961" alt="image" src="https://github.com/user-attachments/assets/f8e98720-1774-4de4-97d7-fa6eb84bf005" />

<img width="1916" height="974" alt="image" src="https://github.com/user-attachments/assets/461bc55b-ac17-4d48-82cd-734be0e9306f" />

<img width="1919" height="965" alt="image" src="https://github.com/user-attachments/assets/3a972982-b509-4a3b-8c40-a84d3cdf176c" />

<img width="1919" height="966" alt="image" src="https://github.com/user-attachments/assets/fdd83993-bfc4-4b9c-98d1-bc740df8256e" />

Healthy Leaf Analysis

<img width="1919" height="965" alt="image" src="https://github.com/user-attachments/assets/8ca22ce7-beb8-4a3e-8c95-3082dde54a77" />

<img width="1919" height="972" alt="image" src="https://github.com/user-attachments/assets/e1b60066-c1d0-4339-8e7b-2e5bf3eb8cad" />

<img width="1919" height="960" alt="image" src="https://github.com/user-attachments/assets/f7bccd3b-558c-4ef3-a58e-da27b32db5b3" />

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
