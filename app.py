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

@app.route('/assistant', methods=['POST'])
def assistant():
    # Obtener el prompt del cuerpo de la petición
    data = request.get_json()
    prompt = data.get('prompt', '')

    # Realizar la solicitud a la API de OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Devolver la respuesta generada
    return jsonify({'response': response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
