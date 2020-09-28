from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')


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


if __name__ == '__main__':
    app.run(debug=True)
