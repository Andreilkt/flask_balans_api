from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    balance = db.Column(db.Integer)
    commission_rate = db.Column(db.Integer, nullable=False)
    URL_webhook = db.Column(db.String(100),)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    status = db.Column(db.String(100), default='Ожидание', nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))



