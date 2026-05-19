from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random

app = FastAPI()

# Frontend ko connect karne ke liye CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AgriVision API is running live!"}

# --- DUMMY PREDICT ENDPOINT FOR FREE RENDER HOSTING ---
@app.post("/predict")
async def predict(file: UploadFile = File(...), lat: float = Form(24.9), lon: float = Form(86.2)):
    # Yeh AI model ki acting karega taaki frontend chalta rahe
    diseases = ["Tomato Late Blight", "Potato Early Blight", "Apple Scab"]
    detected = random.choice(diseases) 
    
    return {
        "disease": detected,
        "confidence": round(random.uniform(85.0, 98.5), 2),
        "severity": "High" if "Blight" in detected else "Medium"
    }

# --- ADMIN MLOPS ENDPOINT ---
@app.get("/admin/stats")
async def get_admin_dashboard_stats():
    return {
        "total_scans": 245,
        "low_confidence_scans": 18,
        "top_diseases": [
            {"name": "Tomato Late Blight", "count": 85},
            {"name": "Potato Early Blight", "count": 60},
            {"name": "Apple Scab", "count": 45}
        ],
        "recent_outbreaks": [
            {"lat": 25.5941, "lon": 85.1376, "disease": "Tomato Late Blight"},
            {"lat": 26.1200, "lon": 85.3640, "disease": "Potato Early Blight"},
            {"lat": 24.7964, "lon": 85.0030, "disease": "Apple Scab"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
