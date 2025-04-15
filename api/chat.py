from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://your-dependencies-app.vercel.app"]}})
load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")

@app.route("/api/chat", methods=["POST"])
def chat():
    query = request.form.get("query")
    if query:
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROK_API_KEY}"},
                json={"model": "grok-3", "messages": [{"role": "user", "content": query}], "max_tokens": 200},
            ).json()["choices"][0]["message"]["content"]
            return {"success": True, "response": response}, 200
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
    return {"success": False, "error": "No query provided"}, 400
