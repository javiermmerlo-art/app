from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)
HF_TOKEN = os.getenv("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")

@app.route("/ai", methods=["POST"])
def ai():
    texto = request.json.get("text", "")
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": texto}

    r = requests.post(
        "https://api-inference.huggingface.co/models/google/flan-t5-small",
        headers=headers,
        json=payload,
        timeout=60
    )

    data = r.json()
    # --- Manejo de errores y formato flexible ---
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        reply = data[0]["generated_text"]
    else:
        # Devuelve todo el JSON de error para depurar
        reply = f"Error en HuggingFace: {data}"

    return jsonify({"reply": reply})
