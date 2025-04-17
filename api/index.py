from fastapi import FastAPI, UploadFile, Form
import requests
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
load_dotenv()

services = {
    "face_detection": os.getenv("FACE_DETECTION_URL", "https://1234.ngrok.io"),
    "video_stream": os.getenv("VIDEO_STREAM_URL", "https://1234.ngrok.io"),
    "tts": os.getenv("TTS_URL", "http://localhost:3000/api/tts")
}

@app.post("/api/add_face")
async def add_face(name: str = Form(...), image: UploadFile = None):
    logger.info(f"Routing add_face to {services['face_detection']}")
    files = {"image": (image.filename, await image.read(), image.content_type)}
    data = {"name": name}
    try:
        response = requests.post(f"{services['face_detection']}/add_face", files=files, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error in add_face: {str(e)}")
        return {"success": False, "error": str(e)}

@app.get("/api/video_feed")
async def video_feed():
    logger.info(f"Routing video_feed to {services['video_stream']}")
    return {"stream_url": f"{services['video_stream']}/video_feed"}

@app.post("/api/generate_tts")
async def generate_tts(text: str = Form(...)):
    logger.info(f"Routing generate_tts to {services['tts']}")
    return {"success": True, "url": "mock://tts/audio.mp3"}  # Mock until real TTS
