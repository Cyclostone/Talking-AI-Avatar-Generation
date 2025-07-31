from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import sys
import os
import asyncio
import json

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app.run_pipeline as pipeline 

app = FastAPI()

class InputText(BaseModel):
    text: str

# Store active WebSocket connections
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_connections.remove(websocket)

async def send_progress(message: str):
    """Send progress updates to all connected WebSocket clients"""
    for connection in active_connections[:]:  # Copy list to avoid modification during iteration
        try:
            await connection.send_text(json.dumps({"status": message}))
        except:
            active_connections.remove(connection)

@app.post("/generate-video")
async def generate_avatar(input: InputText):
    await send_progress("Starting audio generation...")
    audio_path = pipeline.generate_voice(input.text)
    
    await send_progress("Audio generated! Starting video generation...")
    await send_progress("This may take 5-10 minutes. Please wait...")
    
    video_path = pipeline.generate_video()
    
    await send_progress("Video generation complete!")
    return {"audio_path": audio_path, "video_path": video_path}

@app.get("/")
async def root():
    return {"message": "AI Avatar API is running! Connect to /ws for progress updates."}