from flask import Flask, render_template, url_for, flash, redirect
from sqlalchemy import Text, Boolean, Integer, Column, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    book = db.relationship('Books', lazy=True)


    def __repr__(self):
        return f'{self.id}, {self.firstname}, {self.username}, {self.email}, {self.password}'

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique= True, nullable=False)
    author = db.Column(db.String(100), unique= False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.id}, {self.title}, {self.author}, {self.date}'
