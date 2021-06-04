import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = '$DC84J#$JFJ1E$LF0I30RF4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.secret_key = 'SOME_SECRET' 
