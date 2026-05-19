from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...), lat: float = Form(24.9), lon: float = Form(86.2)):
    diseases = ["Tomato Late Blight", "Potato Early Blight", "Apple Scab"]
    return {
        "disease": random.choice(diseases),
        "confidence": round(random.uniform(85.0, 98.5), 2),
        "severity": "High"
    }

@app.get("/admin/stats")
async def get_admin_dashboard_stats():
    return {
        "total_scans": 245,
        "low_confidence_scans": 18,
        "top_diseases": [{"name": "Tomato Late Blight", "count": 85}],
        "recent_outbreaks": [{"lat": 25.5941, "lon": 85.1376, "disease": "Tomato Late Blight"}]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
