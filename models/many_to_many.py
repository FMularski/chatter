from .database import db

"""
table which represents many-to-many relationship users<-->chats
"""

memberships = db.Table('memberships',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True)
                       )

