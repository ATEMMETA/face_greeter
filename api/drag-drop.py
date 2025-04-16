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

@app.route("/api/drag-drop", methods=["POST"])
def drag_drop():
    files = request.files.getlist("files")
    results = []
    for file in files:
        if file and any(file.filename.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png")):
            try:
                name = os.path.splitext(file.filename)[0]
                files = {"image": (file.filename, file.read(), "image/jpeg")}
                data = {"name": name}
                response = requests.post(f"{AI_PROCESSOR_URL}/add_face", files=files, data=data)
                if response.status_code == 200 and response.json()["success"]:
                    conn = sqlite3.connect("db.sqlite")
                    c = conn.cursor()
                    c.execute(
                        "INSERT OR REPLACE INTO faces (name, image, added) VALUES (?, ?, ?)",
                        (name, f"images/{name}.jpg", int(time.time())),
                    )
                    conn.commit()
                    conn.close()
                    os.makedirs("images", exist_ok=True)
                    file.seek(0)
                    with open(f"images/{name}.jpg", "wb") as f:
                        f.write(file.read())
                    results.append({"success": True, "name": name})
                else:
                    results.append({"success": False, "error": "Failed to add face"})
            except:
                results.append({"success": False, "error": "Processing error"})
        else:
            results.append({"success": False, "error": "Invalid file"})
    return {"success": any(r["success"] for r in results), "results": results}, 200 if any(r["success"] for r in results) else 400
