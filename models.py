"""SQLAlchemy Models for User Auth Flask App"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(flask_app):
    db.app = flask_app
    db.init_app(flask_app)

class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feedback = db.relationship('Feedback')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Generates a hash for the given plaintext password and returns a model instance with hashed passwrord"""
        pw_hash = bcrypt.generate_password_hash(password)
        hash_utf8 = pw_hash.decode('utf8')

        return cls(username=username, password=hash_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.get(username)

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete='CASCADE'), nullable=False)