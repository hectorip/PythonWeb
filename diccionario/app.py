# -*- coding: utf-8 -*-
from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Jinja2
    palabra = "Pletórico"
    definicion = "Lleno de algo, especialmente algo bueno."

    context = {
        'palabra': palabra,
        'definicion': definicion,
        'nombre': 'Héctor'
    }

    return render_template('index.html', **context)

@app.route('/word/<value>')
def word(value):
    #Encabezados para la petición de oxford api, nos pide api_id & api_key en los headers
    headers_value = {
        "app_id" : "c4dd8ba2",
        "app_key" : "1484b49aee2bff5132f915ebec6b5acf"
    }

    #Hacemos la petición a la api de oxford
    #result = requests.get('https://od-api.oxforddictionaries.com/api/v1/entries/es/' + palabra, headers=headers_value)
    result = requests.get(f'https://od-api.oxforddictionaries.com/api/v1/entries/es/{value}', headers=headers_value)
    
    if result.status_code != 200:
        print("hubo un problema: ", result.json)

    #si no hubo problema, guardo en una nueva variable la respuesta como JSON
    data = result.json()

    #aquí extraigo el dato que deseo exponer al usuario
    definicion = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"]

    context = {
            'palabra': value,
            'definicion': definicion,
            'nombre': 'Héctor'
        }

    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)