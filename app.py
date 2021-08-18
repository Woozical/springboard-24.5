"""User Auth Flask App"""
from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
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
    return redirect('/login')

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
            session['username'] = new_user.username
            return redirect(f'/user/{new_user.username}')
        except exc.IntegrityError:
            db.session.rollback()
            flash('An account is already registered with that username/email.')
            return redirect('/register')

    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        user =  User.authenticate(form.username.data, form.password.data)
        if user:
            session['username'] = user.username
            return redirect(f'/user/{user.username}')
        else:
            flash('Incorrect login credentials')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/user/<username>')
def user_view(username):
    if 'username' in session:
        user = User.query.get_or_404(username)
        return render_template('user-details.html', user=user)
    else:
        flash('You must be logged in to view user details!')
        return redirect('/')

@app.route('/logout')
def logout_view():
    session.pop('username')
    return redirect('/')

@app.route('/user/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_form_view(username):
    
    if session['username'] != username:
        flash("You are not authorized to view this page")
        return redirect(f'/user/{username}')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        new_feedback = Feedback(
            title=form.title.data, content=form.content.data, username=username
        )
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/user/{username}')
    else:
        return render_template('feedback-form.html', form=form)