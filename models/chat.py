"""
importing global db from separate file
it is used to create model's columns, ex. id = db.Column(...)
"""
from .database import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    """
    one-to-many relationship
    db.relationship() returns a property which can point to multiple instances, 
    here it can point to many Message objects
    
    backref declares additional property 'chat' in Message objects so 
    it is possible to do this:
    some_message_reference.chat which returns the chat where the message
    was written
    
    lazy loading
    True/select: relationships objects are loaded only when they are needed
    False/joined: relationships objects are always loaded with their parents
    """
    messages = db.relationship('Message', backref='chat', lazy=True)

    def __repr__(self):
        return f'{self.id} {self.name} {self.owner_id}'
