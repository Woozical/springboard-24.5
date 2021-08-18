"""User Auth Flask App"""
from flask import Flask, render_template, redirect, flash
from models import db, connect_db, User
from forms import RegisterForm
from sqlalchemy import exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_KEY_HERE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home_view():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User.register(
            username = form.username.data, password = form.password.data,
            email = form.email.data, first_name = form.first_name.data,
            last_name = form.last_name.data
        )

        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect('/secret')
        except exc.IntegrityError:
            db.session.rollback()
            flash('An account is already registered with that username/email.')
            return redirect('/register')

    else:
        return render_template('register.html', form=form)

@app.route('/secret')
def secret_view():
    return "Welcome to the secret"