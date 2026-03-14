from flask import Blueprint, request, jsonify
from config import Config
import requests
from datetime import datetime
from pymongo import MongoClient
import os

ai_bp = Blueprint('ai', __name__)

try:
    client   = MongoClient('mongodb://localhost:27017/')
    mongo_db = client['po_logs']
    ai_logs  = mongo_db['ai_descriptions']
    print("MongoDB connected!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    ai_logs = None

@ai_bp.route('/ai/description', methods=['POST'])
def generate_description():
    try:
        data     = request.get_json()
        name     = data.get('name', '')
        category = data.get('category', 'General')

        if not name:
            return jsonify({"error": "Product name is required"}), 400

        api_key = Config.GEMINI_API_KEY
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        prompt = (
            f"Write exactly 2 professional marketing sentences for a product called "
            f"'{name}' in the '{category}' category. "
            f"Be concise, persuasive, and highlight its value. No bullet points."
        )

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(url, json=payload, timeout=10)
        result   = response.json()
        print("Gemini response:", result)  # debug line
        description = result['candidates'][0]['content']['parts'][0]['text'].strip()

        if ai_logs is not None:
            try:
                ai_logs.insert_one({
                    "product_name": name,
                    "category":     category,
                    "description":  description,
                    "generated_at": datetime.utcnow(),
                    "model":        "gemini-2.0-flash"
                })
                print(f"Logged to MongoDB: {name}")
            except Exception as mongo_err:
                print(f"MongoDB log failed: {mongo_err}")

        return jsonify({"description": description}), 200

    except Exception as e:
        print(f"AI error: {str(e)}")
        return jsonify({"error": str(e)}), 500