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

@app.route('/crear_evento', methods=['POST'])
def crear_evento():
    # Datos que quieres enviar al webhook
    
    webhook_url = 'https://hook.us2.make.com/pqv8e8e6gebzt8kmwytyjr178hwb9qp8l'  # Reemplaza con tu URL real

    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        return jsonify({'status': 'success', 'message': 'Webhook llamado exitosamente.'}), 200
    except requests.exceptions.HTTPError as errh:
        return jsonify({'status': 'error', 'message': f'Error HTTP: {errh}'}), 500
    except requests.exceptions.ConnectionError as errc:
        return jsonify({'status': 'error', 'message': f'Error de conexión: {errc}'}), 500
    except requests.exceptions.Timeout as errt:
        return jsonify({'status': 'error', 'message': f'Tiempo de espera agotado: {errt}'}), 500
    except requests.exceptions.RequestException as err:
        return jsonify({'status': 'error', 'message': f'Error inesperado: {err}'}), 500

    
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
