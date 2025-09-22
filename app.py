from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Lee la variable de entorno HF_TOKEN
HF_TOKEN = os.getenv("HF_TOKEN")

@app.route("/ai", methods=["POST"])
def ai():
    texto = request.json.get("text", "")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": texto}

    try:
        r = requests.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-small",
            headers=headers,
            json=payload,
            timeout=60
        )
    except Exception as e:
        return jsonify({"reply": f"Error al llamar a HuggingFace: {e}"})

    # Depuración: muestra estado y texto crudo
    print("Status code:", r.status_code)
    print("Respuesta bruta:", r.text)

    # Intenta convertir a JSON de forma segura
    try:
        data = r.json()
    except Exception:
        return jsonify({
            "reply": f"No se pudo decodificar JSON. "
                     f"Status: {r.status_code}. "
                     f"Texto: {r.text}"
        })

    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        reply = data[0]["generated_text"]
    else:
        reply = f"Error en HuggingFace: {data}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    # Solo para pruebas locales; en Render se usa gunicorn
    app.run(host="0.0.0.0", port=5000)
