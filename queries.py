from flask import g
from models import User, Books, db
import sqlite3

DATABASE_FILE = '/instance/library.db'

def get_db_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
    return conn

def create_user(firstname, username, email, password):
    user = User(firstname=firstname, username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    
def check_user(email, username):
    email_check = User.query.filter_by(email=email).first()
    username_check = User.query.filter_by(username=username).first()
    return [email_check, username_check]

def find_user(username):
    found_user = User.query.filter_by(username=username).first()
    return found_user

class PasswordCheck:
    def __init__(self, password1, password2):
        self.password1 = password1
        self.password2 = password2
    
    def mismatch(self):
        return self.password1 != self.password2
    
    def not_strong(self):
        return len(self.password1)<6

class EmailCheck:
    def __init__(self, email):
        self.email = email
    
    def invalid(self):
        return "@" not in self.email

def signup_empty(username, email, password, firstname):
    first = firstname == ''
    user = username == ''
    email = email == ''
    pwd = password == ''

    return first or user or email or pwd

def signin_empty(username, password):
    user = username == ''
    pwd = password == ''
    return user or pwd


# working on the books
def get_user_books(user_id):
    all_user_books = Books.query.filter_by(user_id=user_id).all()
    return all_user_books

def add_user_book(title, author, user_id):
    new_book = Books(title=title, author=author, user_id=user_id)
    db.session.add(new_book)
    db.session.commit()

#searching for book
def search_by_title(title, user_id):
    matched_books = Books.query.filter_by(title=title, user_id=user_id).all()
    return matched_books

def search_by_author(author, user_id):
    matched_books = Books.query.filter_by(author=author, user_id=user_id).all()
    return matched_books


def sort_books_by_date():
    new_order = Books.query.order_by(Books.date)
    return new_order

def sort_books_by_title():
    new_order = Books.query.order_by(Books.title)
    return new_order

def sort_books_by_author():
    new_order = Books.query.order_by(Books.author)
    return new_order

def delete_all_books():
    pass

def delete_book():
    pass


def change_book_details(user_id, title, author):
    pass
# editing details
def change_user_details(user_id, firstname, username, email, new_password, current_password):
    pass
