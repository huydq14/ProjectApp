from flask.signals import message_flashed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.fields.core import DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
import email_validator

class SignUpForm(FlaskForm):
    inputFirstName  = StringField('First Name', 
        [DataRequired(message="Please enter your first name!")])
    inputLastName  = StringField('Last Name', 
        [DataRequired(message="Please enter your last name!")])
    inputEmail = StringField('Email address', 
        [Email(message="Not a valid email address"), 
        DataRequired(message="Please enter your email address!")])
    inputPassword = PasswordField('Password', 
        [DataRequired(message="Please enter your password!") ,
        EqualTo('inputConfirmPassword', message="Passwords does not match")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    inputEmail = StringField('Email adress',
        [Email(message="Not a valid email address!"), 
        DataRequired(message="Please enter your email address!")])
    inputPassword = PasswordField('Password',
        [InputRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')

class AddProjectForm(FlaskForm):
    inputName = StringField('Name',
        [InputRequired(message="Enter your Project")])
    inputDescription = StringField('Description',
        [InputRequired(message="Enter your Description!")])
    inputDeadline = StringField('Deadline',
        [InputRequired(message="Enter your project deadline!")])    
    submit = SubmitField('Create')






