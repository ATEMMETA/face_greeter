from flask import Flask, request, jsonify
import requests
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
load_dotenv()

services = {
    "face_detection": os.getenv("API_URL", "https://247f-34-13-145-252.ngrok-free.app"),
    "video_stream": os.getenv("API_URL", "https://247f-34-13-145-252.ngrok-free.app"),
    "tts": os.getenv("TTS_URL", "http://localhost:3000/api/tts")
}

@app.route("/api/add_face", methods=['POST'])
def add_face():
    logger.info(f"Routing add_face to {services['face_detection']}")
    try:
        files = {"image": (request.files['image'].filename, request.files['image'].read(), request.files['image'].content_type)}
        data = {"name": request.form['name']}
        response = requests.post(f"{services['face_detection']}/add_face", files=files, data=data)
        return jsonify(response.json())
    except Exception as e:
        logger.error(f"Error in add_face: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/video_feed", methods=['GET'])
def video_feed():
    logger.info(f"Routing video_feed to {services['video_stream']}")
    return jsonify({"stream_url": f"{services['video_stream']}/video_feed"})

@app.route("/api/generate_tts", methods=['POST'])
def generate_tts():
    logger.info(f"Routing generate_tts to {services['tts']}")
    return jsonify({"success": True, "url": "mock://tts/audio.mp3"})  # Mock until real TTS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
