"""
importing global db from separate file
it is used to create model's columns, ex. id = db.Column(...)
"""
from .database import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.String(32), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_login = db.Column(db.String(128), nullable=False)

    def __init__(self, text, date, chat_id, author_id, author_login):
        self.text = text
        self.date = date
        self.chat_id = chat_id
        self.author_id = author_id
        self.author_login = author_login

    def __repr__(self):
        return f'{self.id} {self.text} {self.chat_id} {self.author_id}'



