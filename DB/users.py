#!flask/bin/python
from datetime import datetime

from app import db

# DATABASE
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    parole = db.Column(db.String(30), nullable=False)
    auto = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id