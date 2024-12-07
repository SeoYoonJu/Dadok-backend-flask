from flask import Blueprint, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()

generate_text_bp = Blueprint('generate_text', __name__)

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in .env file")
openai.api_key = api_key

@generate_text_bp.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    user_input = data.get('prompt')

    if not user_input:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200  
        )

        ai_response =  response.choices[0].message.content
        response = jsonify(ai_response)
        response.headers["Content-Type"] = "application/json; charset=UTF-8"
    
        return response


    except Exception as e:
        print("Error generating text:", e)
        return jsonify({"error": "Failed to generate text"}), 500
