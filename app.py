# app.py
from flask import Flask, request, jsonify
import requests
import openai
#from openai import OpenAI
import os

app = Flask(__name__)

#openai = OpenAI

# Configurar la clave de API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return 'Bienvenido a mi asistente basado en OpenAI.'

@app.route('/create_event', methods=['POST'])
def crear_evento():
    # Datos que quieres enviar al webhook
     
    data = request.get_json()

    if data is None:
        return jsonify({'status': 'error', 'message': 'No se proporcionó un JSON válido en la solicitud.'}), 400


    webhook_url = 'https://hook.us2.make.com/b7voaa155lq42gfzs5v8tooi79xiyb5o'  # Reemplaza con tu URL real

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

    
@app.route('/chat_assistant', methods=['POST'])
def chat_assistant():
    try:
        # Obtener el mensaje del usuario desde la solicitud
        data = request.get_json()

        if data is None or 'message' not in data:
            return jsonify({'status': 'error', 'message': 'Se requiere un campo "message" en el JSON.'}), 400

        user_message = data['message']
        assistant_id = os.environ.get('ASSISTANT_ID')

        if not assistant_id:
            return jsonify({'status': 'error', 'message': 'El ID del asistente no está configurado.'}), 500

        # Llamar a la API de OpenAI
        response = openai.chatCompletion.create(
            model=assistant_id,
            messages=[
                {'role': 'user', 'content': user_message}
            ]
        )

        assistant_reply = response['choices'][0]['message']['content']
        return jsonify({'status': 'success', 'assistant_reply': assistant_reply}), 200

    except Exception as e:
        # Manejar todos los errores inesperados aquí
        return jsonify({'status': 'error', 'message': f'Error inesperado: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
