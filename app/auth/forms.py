from flask_wtf import FlaskForm
from wtforms import (
    StringField, SubmitField, IntegerField, PasswordField, BooleanField
)
from wtforms.validators import DataRequired, Length, Regexp, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 32),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
        'Usersnames must have only letters, numbers, dot or '
        'underscores')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    #age = IntegerField('Age', validators)
    password  = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    telephone = IntegerField('Telephone number', validators=[
        DataRequired(), Length(1, 11),
        Regexp('^[0-9]', 0, 'Telephone should be 11 numbers')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(), EqualTo('password2',
    message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit', validators=[DataRequired()])
