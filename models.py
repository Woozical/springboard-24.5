"""SQLAlchemy Models for User Auth Flask App"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(flask_app):
    db.app = flask_app
    db.init_app(flask_app)

class User(db.Model):

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

