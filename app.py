# Libs
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SESSION_ID = None
SESSION_NAME = None

# DATABASE
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    parole = db.Column(db.String(30), nullable=False)
    auto = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id

# APPLICATION
class App:
    def __init__(self):
        pass

    @app.route('/')
    @app.route('/home')
    def index():
        if SESSION_ID is None and SESSION_NAME is None:
            return redirect('/login')
        else:
            sqluser = db.session.execute("SELECT * FROM users WHERE id = :id", {'id': SESSION_ID})
            user = sqluser.fetchall()
            return render_template("index.html", user=user)

    @app.route('/profile')
    def profile():
        if SESSION_ID is None and SESSION_NAME is None:
            return redirect('/login')
        else: 
            sqluser = db.session.execute("SELECT * FROM users WHERE id = :id", {'id': SESSION_ID})
            user = sqluser.fetchall()
            return render_template("profile.html", user=user)     
    
    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if request.method == "POST":
            name = request.form['name']
            parole = request.form['parole']

            try: 
                sqluser = db.session.execute("SELECT * FROM users WHERE name = :name", {'name': name})
                user = sqluser.fetchall()

                if user[0].parole == parole and user[0].name == name:
                    db.session.execute("UPDATE users SET auto = :auto WHERE name = :name", {
                        'auto': 1,
                        'name': name
                    })
                    db.session.commit()

                    global SESSION_ID
                    SESSION_ID = user[0].id
                    global SESSION_NAME 
                    SESSION_NAME = user[0].name

                    return redirect('/')
                else:
                    return render_template("error.html", error='Данные указаны неверно')
            except:
                return render_template("error.html", error='Произошла ошибка при авторизации')
        else:
            return render_template("login.html")

    @app.route('/register', methods = ['POST', 'GET'])
    def register():
        if SESSION_ID is None and SESSION_NAME is None:
            if request.method == "POST":
                username = request.form['username']
                name = request.form['name']
                parole = request.form['parole']

                md5 = hashlib.new('md5', parole.encode('utf-8'))
                # parole = md5.hexdigest()

                # users = Users(username=username, name=name, parole=parole)

                try:
                    db.session.execute("INSERT INTO users (username, name, parole) VALUES (?, ?, ?)", (username, name, parole))
                    db.session.commit()
                    return redirect('/login')
                except:
                    return render_template("error.html", error='Произошла ошибка при регистрации')
            else: 
                return render_template("register.html")
        else: 
            return redirect('/')

if __name__ == '__main__':
    app.run(port=3000, host='127.0.0.1')