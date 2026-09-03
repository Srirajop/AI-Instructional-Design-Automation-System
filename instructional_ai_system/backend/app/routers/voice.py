from fastapi import APIRouter, UploadFile, File, HTTPException
import re
import os
import base64
import requests

router = APIRouter()

@router.post("/")
async def speech_to_text(audio: UploadFile = File(...)):
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is missing.")
        
    try:
        # Read audio bytes directly into memory (no temp files needed)
        audio_bytes = await audio.read()
        audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # Determine mime type from filename or default to webm since frontend sends webm
        mime_type = "audio/webm"
        if audio.filename.endswith(".mp3"): mime_type = "audio/mp3"
        elif audio.filename.endswith(".wav"): mime_type = "audio/wav"

        # Call Gemini 3.5 Flash Lite REST API directly for lowest cost and fast audio transcription
        # Gemini acts multimodally and can transcribe audio passed as inline data
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Transcribe this audio clip precisely. Return ONLY the raw spoken words. Do NOT include any sound event tags like <noise>, <laughter>, or <silence>. Do not add any introductory or concluding remarks."},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": audio_b64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.0, # Zero temp for most accurate transcription
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        try:
            # Extract the text from the Gemini response structure
            transcription = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Failsafe: Strip out any remaining <tag> markers (like <noise>) that Gemini sometimes injects
            transcription = re.sub(r'<[^>]+>', '', transcription).strip()
            return {"text": transcription}
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Failed to parse Gemini response: " + str(data))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

