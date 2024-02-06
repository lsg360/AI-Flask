from flask import Flask, request, jsonify, render_template
from ai_engine import generate_ai_image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_image", methods=["POST"])
def generate_image():
    data_url = request.json.get("imageDataUrl")
    prompt = request.json.get("prompt")
    
    try:
        base64_image = generate_ai_image(data_url, prompt)
        return jsonify({"base64_image": base64_image})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
