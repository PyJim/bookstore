from flask import Flask, render_template, request, abort, redirect
from models import db, User, Books
from flask_bcrypt import Bcrypt
import sqlite3
from queries import create_user, check_user, PasswordCheck, EmailCheck
from queries import signup_empty, signin_empty, find_user
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # take details from the form is the method is a POST method
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

    # ensuring that only non empty passwords are allowed
        if signup_empty(firstname, username, email, password):
            message = 'please fill all available'
            return render_template('signup.html', message=message)
        
    # checking if password is strong and both passwords match
        user_password = PasswordCheck(password, confirm_password)
        user_email = EmailCheck(email)
        if user_password.mismatch():
            message = 'password mismatch'
            return render_template('signup.html', message=message)
        elif  user_password.not_strong():
            message = 'weak password'
            return render_template('signup.html', message=message)
        elif user_email.invalid():
            message = 'invalid email'
            return render_template('signup.html', message=message)

    # checking if user exists already using email and username which are supposed to be unique
        result1 = check_user(email, username)[0]
        result2 = check_user(email, username)[1]

        if result1 and result2:
            message = f'{email} and {username} already exist'
            return render_template('signup.html', message=message)
        elif result1:
            message = f'{email} already exist'
            return render_template('signup.html', message=message)
        elif result2:
            message = f'{username} already exist'
            return render_template('signup.html', message=message)
        else:
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_user(firstname, username, email, password)
            message = f'Account created successfully'
            return render_template('login.html', message=message)
    # this will be run if the method is a GET method.
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    # ensuring that only non empty passwords are allowed
        if signin_empty(username, password):
            message = 'please fill all available'
            return render_template('login.html', message=message)

        global user
        user = find_user(username)
        correct_password = bcrypt.check_password_hash(user.password, password)
        if user and correct_password:
            return render_template('user.html',user=user.firstname)
        elif user:
            message = 'Invalid password'
            return render_template('login.html',message=message)
        else:
            message = 'Username does not exist'
            return render_template('login.html', message=message)
    return render_template('login.html')

@app.route('/<user_id>', methods=['GET','POST'])
def users():
    if request.method == 'POST':
        global user
        user = None
        return redirect('/')
    
    all_users = User.query.all()
    return render_template('user.html', users = all_users)


if __name__ == '__main__':
    app.run(debug=True)
