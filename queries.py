from flask import g
from models import User, Books, db
import sqlite3

DATABASE_FILE = 'library'

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