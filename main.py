from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np

# Humari dusri files se logic import kar rahe hain
from model_utils import load_saved_model
from xai_pipeline import generate_gradcam

app = FastAPI(title="AgriVision SaaS Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Model yahan load hoga (Phase 1 se)
print("Model Load ho raha hai... Thoda wait karein...")
model = load_saved_model("models/best_model.pth")
print("Model Successfully Load Ho Gaya! 🚀")

# OpenCV Severity Calculator (Phase 2 ka part)
def calculate_leaf_severity(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_disease = np.array([10, 40, 40])
    upper_disease = np.array([30, 255, 255])
    
    mask = cv2.inRange(hsv, lower_disease, upper_disease)
    infected_pixels = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]
    
    severity_pct = (infected_pixels / total_pixels) * 100
    return round(severity_pct, 2)

# Main Prediction Endpoint
@app.post("/predict")
async def predict_crop_disease(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...)
):
    image_bytes = await file.read()
    
    # Severity aur AI Prediction
    severity = calculate_leaf_severity(image_bytes)
    detected_disease = "Tomato Late Blight" # Isko baad me model inference se replace karenge
    confidence_score = 88.4
    
    return {
        "status": "Success",
        "disease": detected_disease,
        "confidence": confidence_score,
        "severity": f"{severity}%",
        "location": {"latitude": lat, "longitude": lon}
    }
# --- PHASE 4: ADMIN MLOPS ENDPOINT ---
@app.get("/admin/stats")
async def get_admin_dashboard_stats():
    # Asaliyat mein yeh data MongoDB ke 'scan_history' collection se aggregate hoga
    return {
        "total_scans": 245,
        "low_confidence_scans": 18, # AI confused in 18 scans (Checking for Model Drift)
        "top_diseases": [
            {"name": "Tomato Late Blight", "count": 85},
            {"name": "Potato Early Blight", "count": 60},
            {"name": "Apple Scab", "count": 45}
        ],
        "recent_outbreaks": [
            # Dummy GPS data based around Bihar for map plotting
            {"lat": 25.5941, "lon": 85.1376, "disease": "Tomato Late Blight"}, # Patna
            {"lat": 26.1200, "lon": 85.3640, "disease": "Potato Early Blight"}, # Muzaffarpur
            {"lat": 24.7964, "lon": 85.0030, "disease": "Apple Scab"}          # Gaya
        ]
    }