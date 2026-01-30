from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from twilio.twiml.messaging_response import MessagingResponse
from ml_engine import SpamClassifier
from llm_engine import LLMClassifier
from time import time
import logging


app = FastAPI(title="AI Scam Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

# ------------------ LOAD MODELS ------------------

ml_engine = SpamClassifier()
llm_engine = LLMClassifier()

# ------------------ RATE LIMITING ------------------

last_calls = {}

def is_rate_limited(user: str, cooldown: int = 3):
    now = time()
    if user in last_calls and now - last_calls[user] < cooldown:
        return True
    last_calls[user] = now
    return False

# ------------------ REQUEST MODEL ------------------

class AnalysisRequest(BaseModel):
    message: str = Field(..., description="The content or text to analyze")
    url: str = Field(None, description="The URL of the page being analyzed")

# ------------------ CORE ANALYSIS FUNCTION ------------------

def run_analysis(text: str, url: str = None):
    # ml_prob = ml_engine.predict(text) # ML engine might need retraining for full page text, keeping it for now but it might be noisy
    # For now, let's just pass 0 or maybe skip ML if it's too long? 
    # Let's keep it simple:
    ml_prob = 0.5 # Placeholder or allow ML to run if text is short enough? 
    # Actually, let's just let ML run, it handles text.
    try:
        ml_prob = ml_engine.predict(text[:2000]) # Truncate for ML to avoid issues
    except:
        ml_prob = 0.0

    analysis = llm_engine.analyze(text, url=url, ml_score=ml_prob)
    analysis["ml_confidence"] = float(ml_prob)
    analysis["ml_model_note"] = "ML model estimates scam-like spam probability"
    return analysis

# ------------------ API ENDPOINTS ------------------

@app.post("/analyze")
async def analyze_message(request: AnalysisRequest):
    try:
        result = run_analysis(request.message, request.url)
        return JSONResponse(result)
    except Exception as e:
        logging.exception("Analysis error")
        raise HTTPException(status_code=500, detail="Analysis failed")

# ------------------ WHATSAPP WEBHOOK ------------------

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(default="unknown")
):
    try:
        if is_rate_limited(From):
            resp = MessagingResponse()
            resp.message("⏳ Please wait a moment before sending another message.")
            return Response(content=str(resp), media_type="application/xml")

        analysis = run_analysis(Body)

        resp = MessagingResponse()
        msg = resp.message()

        reply_text = (
            "⚠️ *SCAM ANALYSIS RESULT*\n\n"
            f"📊 Risk Score: {analysis['risk_score']}/100\n"
            f"🏷️ Type: {analysis['classification']} ({analysis['scam_type']})\n\n"
        )

        if analysis["red_flags"]:
            reply_text += "🚩 *Red Flags:*\n"
            for flag in analysis["red_flags"]:
                reply_text += f"- {flag}\n"

        reply_text += f"\n💡 *Advice:* {analysis['advice']}"

        msg.body(reply_text)

        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        logging.exception("WhatsApp webhook error")
        resp = MessagingResponse()
        resp.message("⚠️ Error analyzing message. Try again later.")
        return Response(content=str(resp), media_type="application/xml")

# ------------------ HEALTH CHECK ------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ------------------ RUN SERVER ------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
