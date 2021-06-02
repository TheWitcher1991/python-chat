# Libs
from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import pretty_errors
import hashlib
import os

app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'SOME_SECRET'


# APPLICATION
class App:
    def __init__(self):
        pass

    @app.route('/')
    @app.route('/home')
    def index():
        if 'username' in session and 'id' in session:
            sqluser = db.session.execute("SELECT * FROM users WHERE id = :id", {'id': session['id']})
            user = sqluser.fetchall()
            return render_template("index.html", user=user)
        else:
            return redirect('/login')

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if 'username' in session and 'id' in session:
            return redirect('/')
        else:
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

                        session['username'] = user[0].name
                        session['id'] = user[0].id

                        return redirect('/')
                    else:
                        return render_template("error.html", error='Данные указаны неверно')
                except:
                    return render_template("error.html", error='Произошла ошибка при авторизации')
            else:
                return render_template("login.html")

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        if 'username' in session and 'id' in session:
            return redirect('/')
        else:
            if request.method == "POST":
                username = request.form['username']
                name = request.form['name']
                parole = request.form['parole']

                if len(username) > 0 and len(name) > 0 and len(parole) >= 5:
                    userkey = uuid4()

                    md5 = hashlib.new('md5', parole.encode('utf-8'))
                    # parole = md5.hexdigest()

                    # users = Users(username=username, name=name, parole=parole)

                    try:
                        sqlif = db.session.execute("SELECT * FROM users WHERE name = :name", {'name': name})
                        row = sqlif.fetchone()

                        if row is None:
                            db.session.execute("INSERT INTO users (username, name, parole, key) VALUES (?, ?, ?, ?)",
                                               (username, name, parole, userkey))
                            db.session.commit()
                            return redirect('/login')
                    except:
                        return render_template("error.html", error='Произошла ошибка при регистрации')
            else:
                return render_template("register.html")

    @app.route('/exit')
    def exit():
        db.session.execute("UPDATE users SET auto = :auto WHERE id = :id", {
            'auto': 0,
            'id': session['id']
        })
        db.session.commit()
        session.pop('username', None)
        session.pop('id', None)
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
