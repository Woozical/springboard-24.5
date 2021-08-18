"""WTForms for User Auth Flask App"""

from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms.fields import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):

    username = StringField("Username",validators=[
        InputRequired(),
        Length(min=3, max=30, message="Username must be between 3 and 30 characters")])
    
    password = PasswordField("Password", validators=[
        InputRequired(),
        Length(min=6, message="Password must be at least 6 characters")])
    
    email = StringField("Email Address", validators=[
        InputRequired(),
        Email(),
        Length(max=50)
    ])

    first_name = StringField("First Name", validators=[
        InputRequired(),
        Length(max=30)
    ])

    last_name = StringField("Last Name", validators=[
    InputRequired(),
    Length(max=30)
    ])