from flask import Flask, render_template, request, redirect, url_for, flash, session
import os


"""
importing models:
importing db, global reference

it is necessary to import all models (here: User, Chat, Message)
as it is important during db.create_all()
"""

from models.database import db
from models.user import User
from models.chat import Chat
from models.message import Message
from datetime import timedelta, datetime


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)


"""
initializing db with app
"""
db.init_app(app)
app.app_context().push()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('home'))

        return render_template('login.html')
    else:
        login_ = request.form['login']
        password = request.form['password']

        user_in_db = User.query.filter_by(login=login_).first()

        if not user_in_db:
            flash('Invalid login. Try again.', category='danger')
            return redirect(url_for('login'))

        if password != user_in_db.password:
            flash('Invalid password. Try again.', category='danger')
            return redirect(url_for('login'))

        session['user_id'] = user_in_db.id
        return redirect(url_for('home'))


@app.route('/logout')
def log_out():
    if 'user_id' in session:
        session.pop('user_id', None)
        flash('Logged out.', category='success')

    return redirect(url_for('login'))


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_in_db = User.query.filter_by(id=session['user_id']).first()
    chats = user_in_db.chats

    return render_template('home.html', login=user_in_db.login, chats=chats)


@app.route('/chat/<chat_id>')
def chat(chat_id):
    chat_ = Chat.query.filter_by(id=chat_id).first()
    user_in_db = User.query.filter_by(id=session['user_id']).first()
    messages = Message.query.filter_by(chat_id=chat_id).all()

    return render_template('chat.html', user=user_in_db, chat=chat_, messages=messages)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('home'))

        return render_template('create_account.html')
    else:
        login_ = request.form['login']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash('Password and password confirmation did not match. Try again.', category='danger')
            return redirect('create_account')

        if User.query.filter_by(login=login_).first():
            flash('Login already exists. Try again.', category='danger')
            return redirect('create_account')

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Try again.', category='danger')
            return redirect('create_account')

        new_user = User(login_, email, password)

        db.session.add(new_user)
        db.session.commit()

        flash('Account has been successfully created. You can now log in.', category='success')

        return redirect(url_for('login'))


@app.route('/find_chat', methods=['GET'])
def find_chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_in_db = User.query.filter_by(id=session['user_id']).first()
    chat_name = request.args.get('chat_name')   # getting form values for method='GET'

    found_chats = []

    if chat_name:
        found_chats = Chat.query.filter_by(name=chat_name).all()

    return render_template('find_chat.html', login=user_in_db.login, found_chats=found_chats)


@app.route('/join_chat/<chat_id>', methods=['POST'])
def join_chat(chat_id):
    chat_ = Chat.query.filter_by(id=chat_id).first()
    user_in_db = User.query.filter_by(id=session['user_id']).first()

    if chat_ in user_in_db.chats:
        flash(f'You are already a member of chat {chat_.name}.', category='danger')
        return redirect(url_for('find_chat'))

    user_joined_message = Message(f'{user_in_db.login} has joined the chat.', datetime.now(),
                                  chat_id=chat_.id, author_id=0)
    chat_.messages.append(user_joined_message)

    chat_.members.append(user_in_db)
    db.session.commit()

    flash(f'You have joined chat {chat_.name}.', category='success')
    return redirect(url_for('home'))


@app.route('/friends', methods=['GET'])
def friends():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_in_db = User.query.filter_by(id=session['user_id']).first()
    
    return render_template('friends.html', login=user_in_db.login, friends=user_in_db.friends)


@app.route('/add_friend', methods=['POST'])
def add_friend():
    friend_login = request.form['friend']

    friend_in_db = User.query.filter_by(login=friend_login).first()

    if not friend_in_db:
        flash(f'{friend_login} not found. Try again.', category='danger')
        return redirect(url_for('friends'))

    user_in_db = User.query.filter_by(id=session['user_id']).first()

    if friend_in_db in user_in_db.friends:
        flash(f'{friend_login} is already your friend.', category='danger')
        return redirect(url_for('friends'))

    user_in_db.friends.append(friend_in_db)
    friend_in_db.friends.append(user_in_db)
    db.session.commit()

    flash(f'{friend_login} is now your friend.', category='success')
    return redirect(url_for('friends'))


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_in_db = User.query.filter_by(id=session['user_id']).first()

        return render_template('create_chat.html', login=user_in_db.login, friends=user_in_db.friends)
    else:
        friends_ids = request.form.getlist('invite_to_chat')    # get ids of members of the new chat

        if len(friends_ids) == 0:
            flash('You must invite at least 1 friend to create a chat. Try again.', category='danger')
            return redirect(url_for('create_chat'))

        user_in_db = User.query.filter_by(id=session['user_id']).first()

        chat_name = request.form['chat_name']
        new_chat = Chat(chat_name, owner_id=user_in_db.id)

        """
        +append the first member of the new chat - the creator
        +assigning creator as the owned !!! property User.owned_chats
        will append the new chat automatically <relationship 1:many> !!!
        """

        new_chat.members.append(user_in_db)
        new_chat.owner = user_in_db

        """
        appending the rest of members
        !!! property User.chats for each User will be automatically updated
        - it will append the new chat
        """

        for friend_id in friends_ids:
            friend = User.query.filter_by(id=friend_id).first()
            new_chat.members.append(friend)

        db.session.add(new_chat)
        db.session.commit()

        flash(f'Chat {chat_name} has been created successfully.', category='success')
        return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
