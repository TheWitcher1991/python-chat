# Libs
import os
import pretty_errors
from uuid import uuid4

from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    session, \
    flash, \
    abort, url_for, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '$DC84J#$JFJ1E$LF0I30RF4'
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
                catch = request.form['captcha']

                try:
                    sqluser = db.session.execute("SELECT * FROM users WHERE name = :name", {'name': name})
                    user = sqluser.fetchall()

                    if check_password_hash(user[0].parole, parole) and user[0].name == name and catch == 'HATEFREE':
                        db.session.execute("UPDATE users SET auto = :auto WHERE name = :name", {
                            'auto': 1,
                            'name': name
                        })
                        db.session.commit()

                        session['username'] = user[0].name
                        session['id'] = user[0].id

                        flash('Авторизация прошла успешно!', category='success')
                        return redirect('/')
                    else:
                        flash('Неверный логин или пароль', category='error')
                except:
                    flash('Произошла ошибка при авторизации', category='error')
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

                if len(username) > 4 and len(name) >= 5 and len(parole) >= 5:
                    userkey = uuid4()

                    hashStr = generate_password_hash(parole)

                    # users = Users(username=username, name=name, parole=parole)

                    try:
                        sqlif = db.session.execute("SELECT * FROM users WHERE name = :name", {'name': name})
                        row = sqlif.fetchone()

                        if row is None:
                            db.session.execute("INSERT INTO users (username, name, parole, key) VALUES (?, ?, ?, ?)",
                                               (username, name, hashStr, userkey))
                            db.session.commit()
                            flash('Регистрация прошла успешно!', category='success') 
                            return redirect('/login')
                    except:
                        flash('Произошла ошибка при регистрации', category='error')
                else:
                    flash('Ошибка введите данные согласно условиям...', category='error')
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
    
    @app.errorhandler(404)
    def pagenot(error):
        if 'username' in session and 'id' in session:
            return redirect('/')
        else: 
            return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='127.0.0.1')
