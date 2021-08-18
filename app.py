"""User Auth Flask App"""
from flask import Flask, render_template, redirect
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_KEY_HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def home_view():
    return redirect('/register')

@app.route('/register')
def register_view():
    form = RegisterForm()
    return render_template('register.html', form=form)