from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
HF_TOKEN = os.getenv("HF_TOKEN")

@app.route("/ai", methods=["POST"])
def ai():
    texto = request.json.get("text", "")
    r = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-small",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": texto}
    )
    return jsonify({"reply": r.json()[0]["generated_text"]})
