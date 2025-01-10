from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), )
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    balance = db.Column(db.Integer)
    commission_rate = db.Column(db.Integer)
    URL_webhook = db.Column(db.String(100))

    def __repr__(self):
        return f'<User {self.username}>'


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    status = db.Column(db.String(100), default='Ожидание', nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
