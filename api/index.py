from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder="../templates", static_folder="../static")
CORS(app, resources={r"/api/*": {"origins": ["https://your-dependencies-app.vercel.app"]}})
load_dotenv()
AI_PROCESSOR_URL = os.getenv("AI_PROCESSOR_URL", "http://placeholder")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Optional

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", ai_processor_url=AI_PROCESSOR_URL)
