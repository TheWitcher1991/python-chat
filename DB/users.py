#!flask/bin/python
from connect import db
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    parole = db.Column(db.String(30), nullable=False)
    key = db.Column(db.Text, nullable=False)
    auto = db.Column(db.Integer, default=0)
    countMSG = db.Column(db.Integer, default=0)
    countFriend = db.Column(db.Integer, default=0)
    countGroup = db.Column(db.Integer, default=0)
    image = db.Column(db.String(30), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id
