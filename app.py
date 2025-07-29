from flask import Flask, request, jsonify, render_template
import openai
import base64
from PIL import Image
import os

# Flask setup
app = Flask(__name__, static_folder='static', template_folder='templates')

# OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt templates for different rewrite tones
persona_templates = {
    "funny": "Rewrite the following dating bio to be funny and charming:",
    "sexy": "Rewrite the following dating bio to be seductive and bold:",
    "professional": "Rewrite the following bio to be polished and career-oriented:",
    "wholesome": "Rewrite the following bio to be kind, sincere, and friendly:",
    "mysterious": "Rewrite the following bio to be intriguing and mysterious:"
}

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Rewrite bio using OpenAI
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

# Rate photo route – placeholder logic
@app.route("/rate-photo", methods=["POST"])
def rate_photo():
    data = request.json
    img_data = data.get("image")

    if not img_data:
        return jsonify({"error": "No image provided"}), 400

    try:
        image_bytes = base64.b64decode(img_data)

        # Placeholder values – replace with ML model in future
        scores = {
            "attractiveness": 8.1,
            "trustworthiness": 8.4,
            "likability": 8.9
        }
        return jsonify(scores)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Frontend route – form page
@app.route("/upload")
def upload():
    return render_template("upload.html")

# Frontend route – results page
@app.route("/results")
def results():
    return render_template("results.html")

# Frontend route – optional waitlist
@app.route("/waitlist")
def waitlist():
    return render_template("waitlist.html")

# Submit handler for HTML form
@app.route("/submit", methods=["POST"])
def submit():
    bio = request.form.get('bio', '')
    tone = request.form.get('tone', 'Professional')
    file = request.files.get('photo')  # currently unused

    # Placeholder transformation result
    rewritten_bio = f"✨ {bio.strip()} (Rewritten in a {tone} tone)"

    return render_template('results.html', rewritten_bio=rewritten_bio)

# Start app
if __name__ == "__main__":
    app.run(debug=True)
