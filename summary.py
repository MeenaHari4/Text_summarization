from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Set your Gemini API key
GEMINI_API_KEY = "AIzaSyB_CRYylxnIGN4fRAR_VYf3dkUMSG1D_Rs"  # 🔑 Add your Gemini API key here
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


class SummarizationRequest(BaseModel):
    text: str
    summary_length: str = "short"  # options: "short", "medium", "detailed"


@app.post(
    "/summarize", 
    tags=["Summarization"],            
    operation_id="summarize_text"      
)
def summarize_text(request: SummarizationRequest):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    # Prompt for summarization
    prompt = (
        f"Summarize the following text in a {request.summary_length} summary:\n\n"
        f"{request.text}"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    summarized_text = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "")
    )

    return {"summary": summarized_text}