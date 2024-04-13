from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    expenses = db.relationship('Expense', backref='user', passive_deletes=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    savings = db.Column(db.Integer, nullable=False)
    wants = db.Column(db.Integer, nullable=False)
    needs = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
