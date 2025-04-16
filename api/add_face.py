from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import sqlite3
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://your-dependencies-app.vercel.app", "https://facegreeter-git-main-lexas-projects-0c10021c.vercel.app"]}})
load_dotenv()
AI_PROCESSOR_URL = os.getenv("AI_PROCESSOR_URL", "http://placeholder")

def init_db():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS faces (name TEXT PRIMARY KEY, image TEXT, added INTEGER)")
    conn.commit()
    conn.close()

init_db()

@app.route("/api/add_face", methods=["POST"])
def add_face():
    if "name" in request.form:
        name = request.form["name"]
        if "image" in request.files:
            image = request.files["image"]
            if any(image.filename.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png")):
                try:
                    files = {"image": (image.filename, image.read(), "image/jpeg")}
                    data = {"name": name}
                    response = requests.post(f"{AI_PROCESSOR_URL}/add_face", files=files, data=data)
                    if response.status_code == 200:
                        result = response.json()
                        if result["success"]:
                            conn = sqlite3.connect("db.sqlite")
                            c = conn.cursor()
                            c.execute(
                                "INSERT OR REPLACE INTO faces (name, image, added) VALUES (?, ?, ?)",
                                (name, f"images/{name}.jpg", int(time.time())),
                            )
                            conn.commit()
                            conn.close()
                            os.makedirs("images", exist_ok=True)
                            image.seek(0)
                            with open(f"images/{name}.jpg", "wb") as f:
                                f.write(image.read())
                            return {"success": True, "message": f"Face added for {name}"}, 200
                        return {"success": False, "error": result["error"]}, 400
                    return {"success": False, "error": "AI processor failed"}, 500
                except Exception as e:
                    return {"success": False, "error": str(e)}, 500
            return {"success": False, "error": "Invalid file type"}, 400
        return {"success": False, "error": "No image uploaded"}, 400
    return {"success": False, "error": "No name provided"}, 400
