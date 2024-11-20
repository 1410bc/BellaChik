# app.py
from flask import Flask, request, jsonify
import requests
import openai
import os

app = Flask(__name__)

# Configurar la clave de API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return 'Bienvenido a mi asistente basado en OpenAI.'

@app.route('/create_event', methods=['POST'])
def send_to_webhook():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400
        
        # URL del webhook de Make
        make_webhook_url = "https://hook.us2.make.com/pqv8e8e6gebzt8kmwytyjr178hwb9qp8l"
        
        # Registra los datos enviados para verificar
        print(f"Datos enviados al webhook: {data}")
        
        # Enviar los datos al webhook
        response = requests.post(make_webhook_url, json=data)
        
        # Registra la respuesta para depuración
        print(f"Respuesta del webhook: {response.status_code}, {response.text}")
        
        return jsonify({
            "status": response.status_code,
            "response": response.text
        })
    except Exception as e:
        # Registrar el error en logs para rastreo
        print(f"Error al enviar al webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

    
@app.route('/ask-assistant', methods=['POST'])
def ask_assistant():
    # Leer la entrada del usuario desde el cuerpo de la solicitud
    user_input = request.get_json().get("message", "")
    
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Llamar al modelo de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # O usa el modelo que prefieras
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Obtener la respuesta generada
        assistant_reply = response['choices'][0]['message']['content']
        
        return jsonify({"response": assistant_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
