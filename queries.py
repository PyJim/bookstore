from flask import Flask, render_template, request, abort, redirect
from models import db, User, Books
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_user(firstname, username, email, password):
    user = User(firstname=firstname, username=username,
                email=email, password=password)
    db.session.add(user)
    db.session.commit()
    
def check_user(email, username):
    email_query = f'SELECT * FROM User WHERE email={email}'
    username_query = f'SELECT * FROM User WHERE username = {username}'
    conn = get_db_connection()
    try:
        result1 = conn.execute(email_query).fetchone()
    except:
        result1 = None
    try:
        result2 = conn.execute(username_query).fetchone()
    except:
        result2 = None
    conn.close()
    return [result1, result2]

def find_user(username, password):
    query = f'SELECT firstname FROM User WHERE username={username} AND password={password}'
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        found_user = cursor.fetchone()
    except:
        found_user = None
    print(found_user)
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