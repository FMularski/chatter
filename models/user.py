"""
importing global db from separate file
it is used to create model's columns, ex. id = db.Column(...)
"""
from .database import db
from .many_to_many import friendships


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)

    """
    one-to-many relationships
    db.relationship() returns a property which can point to multiple instances,
    ex. messages points to many Message objects
    
    backref declares an additional property, here 'owner' of type user in Chat class,
    thanks to that it is possible to do: 
    some_chat_reference.owner which returns the owner of the chat or 
    some_chat.reference.author which returns the author of the message
    
    lazy loading
    True/select: relationships objects are loaded only when they are needed
    False/joined: relationships objects are always loaded with their parents
    """
    owned_chats = db.relationship('Chat', backref='owner', lazy=True)
    messages = db.relationship('Message', backref='author', lazy=True)

    friends = db.relationship('User', secondary=friendships,
                              primaryjoin=friendships.c.user_id == id,
                              secondaryjoin=friendships.c.friend_id == id,
                              backref='users_knowing_this')

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password = password

    def __repr__(self):
        return f'{self.id} {self.login} {self.email} {self.password}'
