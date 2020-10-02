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


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

    return render_template('home.html')


@app.route('/chat/<chat_name>')
def chat(chat_name):
    return render_template('chat.html', chat_name=chat_name)


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


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    if request.method == 'GET':
        return render_template('create_chat.html')
    else:
        pass


@app.route('/find_chat', methods=['GET', 'POST'])
def find_chat():
    if request.method == 'GET':
        return render_template('find_chat.html')
    else:
        pass


@app.route('/friends', methods=['GET', 'POST'])
def friends():
    if request.method == 'GET':
        return render_template('friends.html')
    else:
        pass


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
