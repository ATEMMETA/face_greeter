from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://your-dependencies-app.vercel.app"]}})

@app.route("/api/update_audio", methods=["POST"])
def update_audio():
    try:
        audio = request.files["audio"]
        os.makedirs("static", exist_ok=True)
        audio.save("static/welcome.mp3")
        return {"success": True}, 200
    except Exception as e:
        return {"error": str(e)}, 500
