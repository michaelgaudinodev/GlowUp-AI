from flask import Flask, request, jsonify
import openai
import base64
from PIL import Image

app = Flask(__name__)
openai.api_key = "your_openai_api_key_here"

# Persona style prompts
persona_templates = {
    "funny": "Rewrite the following dating bio to be funny and charming:",
    "sexy": "Rewrite the following dating bio to be seductive and bold:",
    "professional": "Rewrite the following bio to be polished and career-oriented:",
    "wholesome": "Rewrite the following bio to be kind, sincere, and friendly:",
    "mysterious": "Rewrite the following bio to be intriguing and mysterious:"
}

@app.route("/rewrite", methods=["POST"])
def rewrite_bio():
    data = request.json
    bio = data.get("bio")
    style = data.get("style", "professional")
    if not bio:
        return jsonify({"error": "No bio provided"}), 400

    prompt = f"{persona_templates.get(style, persona_templates['professional'])} {bio}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that enhances online personas."},
                {"role": "user", "content": prompt}
            ]
        )
        new_bio = response.choices[0].message["content"].strip()
        return jsonify({"original": bio, "rewritten": new_bio})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/rate-photo", methods=["POST"])
def rate_photo():
    data = request.json
    img_data = data.get("image")
    if not img_data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_bytes = base64.b64decode(img_data)
        # Placeholder scoring logic — use a real ML model later
        scores = {
            "attractiveness": 8.1,
            "trustworthiness": 8.4,
            "likability": 8.9
        }
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
