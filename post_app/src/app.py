# -*- coding: utf-8 -*-
from flask import Flask, render_template
#importamos librería de sqlalchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#establecemos cadena de conexión con la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://127.0.0.1:5432/blog"

#creamos una instancia de la base de datos
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(500), nullable=False)

    #relations
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.title

db.create_all()


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

@app.route('/users/new/<user_name>/<user_email>')
def add_user(user_name, user_email):
    #creo un objeto User nuevo
    user = User(name = user_name, email = user_email)
    #mando aviso de insert a la bd
    db.session.add(user)
    #confirmo el insert
    db.session.commit()

    context = {
        'id' : user.id,
        'name' : user.name,
        'email' : user.email
    }

    return render_template('index.html', **context)

@app.route('/users')
def get_users():
    '''obtengo todos los usuarios
    esto es similar a un select * from user;"
    '''
    users = User.query.all()

    context = {
        'users' : users
    }

    return render_template('user_lists.html', **context)

@app.route('/posts/new/<title>/<body>/<user>/')
def new_post(title, body, user):
    #filter: consulta de filtrado
    user = User.query.filter_by(id = user).first()
    new_post = Post(title = title, body = body, user = user)
    db.session.add(new_post)
    db.session.commit()

    context = {
        'id' : new_post.id,
        'title' : new_post.title,
        'body' : new_post.body,
        'user' : new_post.user.name,
        'email' : new_post.user.email
    }

    return render_template('post.html', **context)

@app.route('/posts')
def get_post():

    posts = Post.query.all()
    
    context = {
        'posts' : posts
    }

    return render_template('posts.html', **context)

if __name__ == '__main__':
    app.run(debug=True)