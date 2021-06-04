#!flask/bin/python
from datetime import datetime
from app import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    key = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(30), nullable=True)
    countmsg = db.Column(db.Integer, default=0)
    countusers = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Group %r>' % self.id
