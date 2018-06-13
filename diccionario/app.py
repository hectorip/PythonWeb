# -*- coding: utf-8 -*-
from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True)