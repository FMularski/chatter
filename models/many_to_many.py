from .database import db

"""
table which represents many-to-many relationship users<-->chats
"""

memberships = db.Table('memberships',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                       db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), nullable=False)
                       )

"""
table which represents many-to-many relationship users<-->users
"""
friendships = db.Table('friendships',
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                       db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
                       )

