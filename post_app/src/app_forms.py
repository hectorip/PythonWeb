# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
#importamos librería de sqlalchemy
from flask_sqlalchemy import SQLAlchemy

#forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#end forms

app = Flask(__name__)

#establecemos cadena de conexión con la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://127.0.0.1:5432/blog"
app.config['WTF_CSRF_SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
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

#forms objects
class UserForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    submit = SubmitField('Save it')

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

@app.route('/users/new', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    
    if form.validate_on_submit():
        print(form)
        #creo un objeto User nuevo
        user = User(name = form.name.data, email = form.email.data)
        print(user)
        #mando aviso de insert a la bd
        db.session.add(user)
        #confirmo el insert
        db.session.commit()


        context = {
            'id' : user.id,
            'name' : user.name,
            'email' : user.email,
            'form': UserForm()
        }


        return render_template('index.html', **context,)
    else:
        print(form.name, "not valid")
    return render_template('index.html', form=form)


    

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