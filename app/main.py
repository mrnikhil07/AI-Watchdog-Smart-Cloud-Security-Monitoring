# app/main.py
from fastapi import FastAPI, Request
import joblib

app = FastAPI()

# Try loading your model -- replace path if needed
try:
    model = joblib.load("models/anomaly_model.joblib")
except Exception:
    model = None

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    logs = data.get("logs", [])

    # TODO: replace this with your real feature extraction + prediction
    score = 0.0
    if model:
        # build features from logs and call model.predict_proba / model.predict
        score = 0.9

    return {"anomaly_score": score, "alerts": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
