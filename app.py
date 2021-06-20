#!flask/bin/python

# -*- coding: utf-8 -*-

""" 
    :version: 1.0.0
    :see: https://github.com/TheWitcher1991/HateFree
"""


from uuid import uuid4
from flask import render_template, \
    request, \
    redirect, \
    session, \
    flash
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

from connect import db, app
from DB.users import Users


# APPLICATION
class App:
    def __init__(self):
        pass

    @app.route('/')
    @app.route('/home')
    def index():
        if 'username-k' in session and 'id-k' in session:
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
                        session['session_n_key'] = Fernet.generate_key()
                        session['username-k'] = f"{user[0].name}-{session['session_n_key']}"
                        session['id'] = user[0].id
                        session['session_i_key'] = Fernet.generate_key()
                        session['id-k'] = f"{user[0].id}-{session['session_i_key']}"

                        flash('Авторизация прошла успешно!', category='success')
                        return redirect('/')
                    else:
                        return flash('Неверный логин или пароль', category='error')
                except:
                    return flash('Произошла ошибка при авторизации', category='error')
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
                catch = request.form['captcha']

                if len(username) > 4 and len(name) >= 5 and len(parole) >= 5 and catch == 'HATEFREE':
                    userkey = uuid4()

                    hashStr = generate_password_hash(parole)

                    users = Users(username=username, name=name, parole=hashStr, key=userkey)

                    try:
                        # db.session.execute("INSERT INTO users (username, name, parole, key) VALUES (?, ?, ?, ?)",
                        #                   (username, name, hashStr, userkey))
                        db.session.add(Users)
                        db.session.commit()

                        flash('Регистрация прошла успешно!', category='success')
                        return users
                    except:
                        return flash('Произошла ошибка при регистрации', category='error')
                else:
                    return flash('Ошибка введите данные согласно условиям...', category='error')
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
