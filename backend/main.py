from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import os
import uvicorn

# Try tflite_runtime first, fall back to full tensorflow
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow as tf
    tflite = tf.lite

# ── Config ────────────────────────────────────────────────────────────────────

MODEL_PATH    = os.path.join(os.path.dirname(__file__), "model", "plant_model.tflite")
IMAGE_SIZE    = 224
MAX_FILE_SIZE = 10 * 1024 * 1024   # 10 MB hard limit

CLASS_NAMES = [
    "Bell Pepper - Bacterial Spot",
    "Bell Pepper - Healthy",
    "Potato - Early Blight",
    "Potato - Late Blight",
    "Potato - Healthy",
    "Tomato - Bacterial Spot",
    "Tomato - Early Blight",
    "Tomato - Late Blight",
    "Tomato - Leaf Mold",
    "Tomato - Septoria Leaf Spot",
    "Tomato - Spider Mites",
    "Tomato - Target Spot",
    "Tomato - Yellow Leaf Curl Virus",
    "Tomato - Mosaic Virus",
    "Tomato - Healthy",
]

DISEASE_META = {
    "Bell Pepper - Bacterial Spot":    {"severity_factor": 0.75, "spread_factor": 0.85, "treatment": "Remove infected leaves. Apply copper-based bactericide."},
    "Bell Pepper - Healthy":           {"severity_factor": 0.00, "spread_factor": 0.00, "treatment": "Plant is healthy. Maintain regular care."},
    "Potato - Early Blight":           {"severity_factor": 0.55, "spread_factor": 0.65, "treatment": "Apply chlorothalonil fungicide. Remove lower infected leaves."},
    "Potato - Late Blight":            {"severity_factor": 0.95, "spread_factor": 0.95, "treatment": "Destroy infected plants immediately. Apply mancozeb fungicide."},
    "Potato - Healthy":                {"severity_factor": 0.00, "spread_factor": 0.00, "treatment": "Plant is healthy. Maintain regular care."},
    "Tomato - Bacterial Spot":         {"severity_factor": 0.70, "spread_factor": 0.75, "treatment": "Avoid overhead watering. Use copper-based spray."},
    "Tomato - Early Blight":           {"severity_factor": 0.60, "spread_factor": 0.70, "treatment": "Apply fungicide. Improve air circulation."},
    "Tomato - Late Blight":            {"severity_factor": 0.95, "spread_factor": 0.95, "treatment": "Remove all infected tissue. Apply systemic fungicide immediately."},
    "Tomato - Leaf Mold":              {"severity_factor": 0.65, "spread_factor": 0.70, "treatment": "Reduce humidity. Apply fungicide."},
    "Tomato - Septoria Leaf Spot":     {"severity_factor": 0.65, "spread_factor": 0.72, "treatment": "Remove infected leaves. Apply copper or chlorothalonil."},
    "Tomato - Spider Mites":           {"severity_factor": 0.70, "spread_factor": 0.80, "treatment": "Apply miticide or neem oil. Keep plants well-watered."},
    "Tomato - Target Spot":            {"severity_factor": 0.65, "spread_factor": 0.68, "treatment": "Apply fungicide. Remove heavily infected leaves."},
    "Tomato - Yellow Leaf Curl Virus": {"severity_factor": 0.92, "spread_factor": 0.90, "treatment": "No cure. Remove infected plants. Control whitefly vectors."},
    "Tomato - Mosaic Virus":           {"severity_factor": 0.90, "spread_factor": 0.88, "treatment": "No cure. Remove infected plants. Disinfect all tools."},
    "Tomato - Healthy":                {"severity_factor": 0.00, "spread_factor": 0.00, "treatment": "Plant is healthy. Maintain regular care."},
}

# ── Model (loaded once at startup) ────────────────────────────────────────────

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Plant Disease Detection API",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — read allowed origins from environment variable so it's easy to update
# Set ALLOWED_ORIGINS in Render dashboard, e.g.:
#   https://your-app.vercel.app,http://localhost:3000
_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

interpreter = None

interpreter = None

@app.on_event("startup")
def load_model():
    global interpreter

    print("Loading model from:", MODEL_PATH)

    try:
        interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        print("✅ Model loaded successfully!")
    except Exception as e:
        print("❌ Failed to load model:", str(e))
        interpreter = None

# ── Helpers ───────────────────────────────────────────────────────────────────

def preprocess(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    array = np.array(image, dtype=np.float32) / 255.0
    return np.expand_dims(array, axis=0)

def run_inference(input_data: np.ndarray) -> np.ndarray:
    input_details  = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]["index"])[0]

def parse_label(label: str):
    if " - " in label:
        plant, disease = label.split(" - ", 1)
    else:
        plant, disease = "Unknown", label
    return plant, disease

def compute_percentages(class_label: str, confidence: float):
    meta            = DISEASE_META.get(class_label, {"severity_factor": 0.5, "spread_factor": 0.5})
    severity_pct    = min(100, round(confidence * meta["severity_factor"] * 100))
    progression_pct = min(100, round(severity_pct * meta["spread_factor"]))
    return severity_pct, progression_pct

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Plant Disease Detection API v2 is running"}

@app.get("/health")
def health():
    return {"model_loaded": interpreter is not None}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Guard: model available
    if interpreter is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Try again shortly.")

    # Guard: must be an image
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (jpg, png, etc.)")

    # Read and size-check
    image_bytes = await file.read()
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Image too large. Maximum size is 10 MB.")

    # Preprocess + inference
    try:
        input_data = preprocess(image_bytes)
        scores     = run_inference(input_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

    # Results
    predicted_index = int(np.argmax(scores))
    confidence      = float(scores[predicted_index])
    confidence_pct  = round(confidence * 100, 1)
    class_label     = CLASS_NAMES[predicted_index]
    plant, disease  = parse_label(class_label)

    severity_pct, progression_pct = compute_percentages(class_label, confidence)

    meta      = DISEASE_META.get(class_label, {})
    treatment = meta.get("treatment", "Consult an agricultural expert.")

    top3_indices = np.argsort(scores)[::-1][:3]
    top3 = [
        {"label": CLASS_NAMES[i], "confidence": round(float(scores[i]) * 100, 1)}
        for i in top3_indices
    ]

    return JSONResponse({
        "plant":       plant,
        "disease":     disease,
        "confidence":  confidence_pct,
        "severity":    severity_pct,
        "progression": progression_pct,
        "treatment":   treatment,
        "top3":        top3,
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
