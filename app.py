from flask import Flask, render_template, request

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


"""
initializing db with app
"""
db.init_app(app)
app.app_context().push()


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/chat/<chat_name>')
def chat(chat_name):
    return render_template('chat.html', chat_name=chat_name)


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
        return render_template('create_account.html')
    else:
        login_ = request.form['login']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        return f'{login_}\n{email}\n{password}\n{confirm}'


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

