from flask import Flask, render_template, request, abort, redirect
from models import db, User, Books
from flask_bcrypt import Bcrypt
import sqlite3
from queries import create_user, check_user, PasswordCheck, EmailCheck
from queries import signup_empty, signin_empty, find_user
from queries import get_user_books, add_user_book, change_user_details


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
            return redirect(f'/{user.username}')
        elif user:
            message = 'Invalid password'
            return render_template('login.html',message=message)
        else:
            message = 'Username does not exist'
            return render_template('login.html', message=message)
    return render_template('login.html')

@app.get('/logout')
def logout():
    global user
    user = None
    return redirect('/')

@app.route('/<username>', methods=['GET','POST'])
def users(username):
    user = find_user(username)
    if user:
        user_id = user.id
        current_user = User.query.filter_by(id=user_id).first().firstname
        books = get_user_books(user_id)
        book_titles = [book.title for book in books]
        book_authors = [book.author for book in books]
        book_dates = [book.date for book in books]
        return render_template('user.html', titles=book_titles, authors=book_authors, dates=book_dates, current_user=current_user)
    else:
        message = 'Username does not exist'
        return render_template('login.html', message=message)

@app.get('/add')
def add():
    return render_template('add.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        
        if title and author:
            title, author = title.capitalize(), author.capitalize()
            add_user_book(title=title, author=author, user_id=user.id)
    return redirect(f'/<{user.id}>')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_user_profile():
    global user
    email = user.email
    username = user.username
    firstname = user.firstname

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        return change_user_details(user_id=user.id, firstname=firstname, username=username, email=email, new_password=new_password, current_password=current_password)


    return render_template('edit_user_profile.html',email=email,username=username, firstname=firstname)




if __name__ == '__main__':
    app.run(debug=True)
