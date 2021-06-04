#!flask/bin/python
from datetime import datetime
from app import db


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    key = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    personalname = db.Column(db.String(30), nullable=False)
    personalrid = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Personal %r>' % self.id
