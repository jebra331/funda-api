from fastapi import FastAPI
import time

app = FastAPI()

funda_data = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    "funda_score": 1.0,
    "sentiment": "صعودی ملایم",
    "confidence": 85,
    "summary": "تحلیل لحظه‌ای طلا...",
    "price_now": 4968
}

@app.get("/")
async def root():
    return {"message": "Funda Score API is running!", "status": "active"}

@app.get("/api/funda")
async def get_funda():
    return funda_data

