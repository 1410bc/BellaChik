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
        from pprint import pprint  # Asegúrate de importar pprint

        # Obtener el mensaje del usuario desde la solicitud
        data = request.get_json()

        if data is None or 'message' not in data:
            return jsonify({'status': 'error', 'message': 'Se requiere un campo "message" en el JSON.'}), 400

        user_message = data['message']
        assistant_id = os.getenv("ASSISTANT_ID")

        # Crear un hilo de conversación
        thread = openai.beta.threads.create()

        # Agregar el mensaje del usuario al hilo
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message,
        )

        # Ejecutar el asistente
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        # Verificar el estado de la ejecución
        while run.status not in ("completed", "failed", "requires_action"):
            run = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )

        # Obtener los mensajes de la conversación
        messages = openai.beta.threads.messages.list(
            thread_id=thread.id,
        )

        # Construir la respuesta
        responses = []
        for each in messages:
            role = each.role
            content = each.content[0].text.value
            responses.append({'role': role, 'content': content})
            pprint(f"{role}: {content}")  # Imprimir en consola para depuración

        # Retornar los mensajes como respuesta
        return jsonify({'status': 'success', 'messages': responses}), 200

    except Exception as e:
        # Manejar errores inesperados
        return jsonify({'status': 'error', 'message': f'Error inesperado: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
