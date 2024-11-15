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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
