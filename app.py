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

    # --- Log de depuración ---
    print("Status code:", r.status_code)
    print("Raw text:", r.text)

    try:
        data = r.json()
    except Exception as e:
        return jsonify({"reply": f"Error: no se pudo decodificar JSON. Status {r.status_code}. Respuesta: {r.text}"})

    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        reply = data[0]["generated_text"]
    else:
        reply = f"Error en HuggingFace: {data}"

    return jsonify({"reply": reply})

