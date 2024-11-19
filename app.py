# app.py
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configurar la clave de API de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return 'Bienvenido a mi asistente basado en OpenAI.'

@app.route('/webhook', methods=['POST'])
def send_to_webhook():
    # URL del webhook de Make
    make_webhook_url = "https://hook.us2.make.com/pqv8e8e6gebzt8kmwytyjr178hwb9qp8"
    
    # Datos enviados desde el cliente
    data = request.get_json()
    
    # Opcional: puedes validar o procesar los datos aquí.
    
    # Enviar datos al webhook
    response = requests.post(make_webhook_url, json=data)
    
    return jsonify({
        "status": response.status_code,
        "response": response.text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
